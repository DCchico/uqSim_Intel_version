#include <iostream>
#include <algorithm>
#include <assert.h>

#include "time_model.hh"

void
TimeModel::reset(Time newLatency) {
	return;
}

/************** ExpoTimeModel ****************/

ConstTimeModel::ConstTimeModel(Time latency): latency(latency), curLatency(latency) {}

Time
ConstTimeModel::lat() {
	return curLatency;
}

void
ConstTimeModel::setFreq(unsigned baseFreq, unsigned curFreq, double scaleFactor) {
	curLatency = (Time)( (1.0 - scaleFactor + scaleFactor * (double)baseFreq/(double)curFreq) * latency );
}

/************** ExpoTimeModel ****************/

ExpoTimeModel::ExpoTimeModel(Time latency): latency(latency),  curLatency(latency), lambda(1.0/latency) {
	int sd = std::chrono::system_clock::now().time_since_epoch().count();
	gen.seed(sd);
	dist = std::exponential_distribution<double> (lambda);
}

void
ExpoTimeModel::reset(Time newLatency) {
	if(curLatency != newLatency) {
		curLatency = newLatency;
		lambda = 1.0/curLatency;

		int sd = std::chrono::system_clock::now().time_since_epoch().count();
		gen.seed(sd);
		dist = std::exponential_distribution<double> (lambda);
	}	
}

void
ExpoTimeModel::setFreq(unsigned baseFreq, unsigned curFreq, double scaleFactor) {
	std::cout << "ExpoTimeModel curFreq set to " << curFreq << std::endl;
	Time lat = (Time)( latency*(1.0 - scaleFactor + scaleFactor * (double)baseFreq/(double)curFreq) );
	reset(lat);
}

Time
ExpoTimeModel::lat() {
	return (Time)dist(gen);
}

/***************** Histogram **********************/
void
Histogram::setTimeDistr(std::vector<Time> distr) {
	assert(!epoll_like);
	time_distr = distr;
	assert(time_distr.size() == 100);
}

void
Histogram::setTimeMap(std::unordered_map<unsigned, Time> time_map, std::vector<unsigned> ekeys) {
	assert(epoll_like);
	event_time_map = time_map;
	event_keys = ekeys;
}

Time
Histogram::getTime(unsigned num_event) {
	if(epoll_like) {
		if(std::find(event_keys.begin(), event_keys.end(), num_event) != event_keys.end()) {
			// std::cout << "hist getTime event num = " << num_event << std::endl;
			return event_time_map[num_event];
		} else {
			unsigned i = 0;
			while(i < event_keys.size()) {
				if(event_keys[i] > num_event)
					break;
				i += 1;
			}

			if(i == 0 || i >= event_keys.size()) {
				unsigned pos = 0;
				if(i >= event_keys.size())
					pos = event_keys.size() - 1;
				unsigned fit_event_cnt = event_keys[pos];
				// std::cout << "hist getTime fitted event num = " << fit_event_cnt << std::endl;
				return event_time_map[fit_event_cnt];
			} else {
				unsigned lower_eve = event_keys[i - 1];
				unsigned upper_eve = event_keys[i];
				if(upper_eve - num_event < num_event - lower_eve) {
					Time t = event_time_map[upper_eve];
					// std::cout << "hist getTime upper event num = " << upper_eve << std::endl;
					assert(t != 0);
					return t;
				} else {
					Time t = event_time_map[lower_eve];
					// std::cout << "hist getTime lower event num = " << lower_eve << std::endl;
					assert(t != 0);
					return t;
				} 
					
			}
		}
	} else {
		int num = rand() % 100;
		// std::cout << "hist getTime random num = " << num << std::endl;
		return time_distr[num];
	}
}

void
Histogram::show() {
	if(!epoll_like) {
		for(unsigned i = 0; i < 100; ++i) 
			// printf("%lu\n", hist[i]);
			printf("%d%% : %lu ns\n", i, time_distr[i]);
		printf("\n");
	} else {
		// printf("histogram for %s:\n", stageName.c_str());
		for(unsigned i = 0; i < event_keys.size(); ++i) 
			// printf("%lu\n", hist[i]);
			printf("%d : %lu ns\n", event_keys[i], event_time_map[event_keys[i]]);
		printf("\n");
	}
}

/***************** HistRecord **********************/
void
HistRecord::addHist(Histogram hist, unsigned freq, uint64_t qps) {
	if( std::find(freq_included.begin(), freq_included.end(), freq) == freq_included.end()) {
		freq_included.push_back(freq);
		std::sort(freq_included.begin(), freq_included.end());
		per_freq_qps_included[freq] = std::vector<uint64_t> ();
	}

	if(qps != 0 && 
		std::find(per_freq_qps_included[freq].begin(), per_freq_qps_included[freq].end(), qps) 
			== per_freq_qps_included[freq].end()) {
		per_freq_qps_included[freq].push_back(qps);
		std::sort(per_freq_qps_included[freq].begin(), per_freq_qps_included[freq].end());
	}

	std::string key = std::to_string(freq) + "MHz";
	if(qps != 0)
		key += "_" + std::to_string(qps) + "qps";
	histograms[key] = hist;
}

Histogram
HistRecord::getHist(unsigned freq, uint64_t qps) {
	assert(freq > 0);
	std::string key = std::to_string(freq) + "MHz_" + std::to_string(qps) + "qps";
	if(histograms.find(key) != histograms.end()) {

		// for debug
		std::cout << "get hist for " << key << std::endl;

		return histograms[key];
	} else {
		// assume frequency must exists
		assert(std::find(freq_included.begin(), freq_included.end(), freq) != freq_included.end());
		// try to find the closest qps if exists
		if(!per_freq_qps_included[freq].empty()) {
			unsigned i = 0;
			while(i < per_freq_qps_included[freq].size()) {
				if(per_freq_qps_included[freq][i] > qps)
					break;
				i += 1;
			}
			if(i >= per_freq_qps_included[freq].size() || i == 0) {
				unsigned pos = 0;
				if(i >= per_freq_qps_included[freq].size())
					pos = per_freq_qps_included[freq].size() - 1;
				unsigned fit_qps = per_freq_qps_included[freq][pos];
				key = std::to_string(freq) + "MHz_" + std::to_string(fit_qps) + "qps";
				assert(histograms.find(key) != histograms.end());

				// for debug
				std::cout << "get hist for " << key << std::endl;

				return histograms[key];
			} else {
				unsigned lower_qps = per_freq_qps_included[freq][i - 1];
				unsigned upper_qps = per_freq_qps_included[freq][i];

				if(upper_qps - qps < qps - lower_qps)
					key = std::to_string(freq) + "MHz_" + std::to_string(upper_qps) + "qps";
				else
					key = std::to_string(freq) + "MHz_" + std::to_string(lower_qps) + "qps";
				assert(histograms.find(key) != histograms.end());

				// for debug
				std::cout << "get hist for " << key << std::endl;
				return histograms[key];
			}
		} else {
			key = std::to_string(freq) + "MHz";

			// for debug
			std::cout << "get hist for " << key << std::endl;

			assert(histograms.find(key) != histograms.end());
			return histograms[key];
		}
		
	}
}
