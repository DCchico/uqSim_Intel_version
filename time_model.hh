#ifndef __TIME_MODEL_HH__
#define __TIME_MODEL_HH__

#include <random>
#include <chrono>
#include <vector>
#include <unordered_map>

#include "util.hh"

class TimeModel 
{
	public:
		virtual ~TimeModel() {}
		virtual Time lat() = 0;
		virtual void reset(Time newLatency);

		virtual void setFreq(unsigned baseFreq, unsigned curFreq, double scaleFactor) = 0;
		virtual Time getLat() = 0;

};

class ConstTimeModel: public TimeModel
{
	protected:
		Time latency;
		Time curLatency;
	
	public:
		ConstTimeModel(Time latency);
		Time lat() override;
		void setFreq(unsigned baseFreq, unsigned curFreq, double scaleFactor) override;
		Time getLat() override {return curLatency;}
};

class ExpoTimeModel: public TimeModel
{
	protected:
		Time latency;
		Time curLatency;
		double lambda;

		std::exponential_distribution<double> dist;
		std::default_random_engine gen;
	
	public:
		ExpoTimeModel(Time latency);
		void reset(Time newLatency) override;
		Time lat() override;
		void setFreq(unsigned baseFreq, unsigned curFreq, double scaleFactor) override;
		Time getLat() override {return curLatency;}
};

class Histogram
{
	protected:
		bool epoll_like;
		std::vector<Time> time_distr;
		std::unordered_map<unsigned, Time> event_time_map;
		std::vector<unsigned> event_keys;

	public:
		Histogram(): epoll_like(false) {}
		Histogram(bool epoll): epoll_like(epoll) {}
		bool isEpollLike() { return epoll_like; }
		void setTimeDistr(std::vector<Time> distr);
		void setTimeMap(std::unordered_map<unsigned, Time> time_map, std::vector<unsigned> ekeys);
		Time getTime(unsigned num_event);

		void show();
};

class HistRecord
{
	public:
		std::vector<unsigned> freq_included;
		std::unordered_map<unsigned, std::vector<uint64_t>> per_freq_qps_included;
		std::unordered_map<std::string, Histogram> histograms;

		HistRecord() {}
		// qps = 0 means matching all qps at that freq
		void addHist(Histogram hist, unsigned freq, uint64_t qps);
		Histogram getHist(unsigned freq, uint64_t qps);
};

#endif