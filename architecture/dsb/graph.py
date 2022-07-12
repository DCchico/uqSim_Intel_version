import sys
import os
import json
import make_arch as march 


def main():
	sched = march.make_service_sched("CMT", [8, [20,21,22,23,24,25,26,27]], None)
	nginx = march.make_serv_inst(servName = "nginx", servDomain = "", instName = "nginx", 
		modelName = "nginx", sched = sched, machId = 0)

	sched = march.make_service_sched("CMT", [2, [28,29]], None)
	unique_id = march.make_serv_inst(servName = "unique_id", servDomain = "", instName = "unique_id", 
		modelName = "unique_id", sched = sched, machId = 1)

	sched = march.make_service_sched("CMT", [2, [30,31]], None)
	url_shorten = march.make_serv_inst(servName = "url_shorten", servDomain = "", instName = "url_shorten", 
		modelName = "url_shorten", sched = sched, machId = 2)
	
	sched = march.make_service_sched("CMT", [4, [32,33,34,35]], None)
	media = march.make_serv_inst(servName = "media", servDomain = "", instName = "media", 
		modelName = "media", sched = sched, machId = 3)

	sched = march.make_service_sched("CMT", [4, [36,37,38,39]], None)
	text = march.make_serv_inst(servName = "text", servDomain = "", instName = "text", 
		modelName = "text", sched = sched, machId = 4)

	sched = march.make_service_sched("CMT", [2, [20,21]], None)
	user_tag = march.make_serv_inst(servName = "user_tag", servDomain = "", instName = "user_tag", 
		modelName = "user_tag", sched = sched, machId = 5)

	sched = march.make_service_sched("CMT", [2, [22,23]], None)
	recommend = march.make_serv_inst(servName = "recommend", servDomain = "", instName = "recommend", 
		modelName = "recommend", sched = sched, machId = 6)

	sched = march.make_service_sched("CMT", [4, [24,25,26,27]], None)
	read_home_t = march.make_serv_inst(servName = "read_home_t", servDomain = "", instName = "read_home_t", 
		modelName = "read_home_t", sched = sched, machId = 7)

	sched = march.make_service_sched("CMT", [6, [28,29,30,31,32,33]], None)
	compose_post = march.make_serv_inst(servName = "compose_post", servDomain = "", instName = "compose_post", 
		modelName = "compose_post", sched = sched, machId = 8)

	sched = march.make_service_sched("CMT", [2, [34,35]], None)
	user_timeline = march.make_serv_inst(servName = "user_timeline", servDomain = "", instName = "user_timeline", 
		modelName = "user_timeline", sched = sched, machId = 9)

	sched = march.make_service_sched("CMT", [2, [36,37]], None)
	write_home_timeline = march.make_serv_inst(servName = "write_home_timeline", servDomain = "", instName = "write_home_timeline", 
		modelName = "write_home_timeline", sched = sched, machId = 10)
	
	sched = march.make_service_sched("CMT", [2, [38,39]], None)
	user = march.make_serv_inst(servName = "user", servDomain = "", instName = "user", 
		modelName = "user", sched = sched, machId = 11)

	sched = march.make_service_sched("CMT", [4, [20,21,22,23]], None)
	social_graph = march.make_serv_inst(servName = "social_graph", servDomain = "", instName = "social_graph", 
		modelName = "social_graph", sched = sched, machId = 12)

	sched = march.make_service_sched("CMT", [2, [24,25]], None)
	post_storage = march.make_serv_inst(servName = "post_storage", servDomain = "", instName = "post_storage", 
		modelName = "post_storage", sched = sched, machId = 13)

	sched = march.make_service_sched("CMT", [1, [26]], None)
	rabbit_mq = march.make_serv_inst(servName = "rabbit_mq", servDomain = "", instName = "rabbit_mq", 
		modelName = "rabbit_mq", sched = sched, machId = 14)

	sched = march.make_service_sched("CMT", [8, [27,28,29,30,31,32,33,34]], None)
	memcached = march.make_serv_inst(servName = "memcached", servDomain = "", instName = "memcached", 
		modelName = "memcached", sched = sched, machId = 15)

	sched = march.make_service_sched("CMT", [300, [35,36,37,38]], None)
	mongodb = march.make_serv_inst(servName = "mongodb", servDomain = "", instName = "mongodb", 
		modelName = "mongodb", sched = sched, machId = 16)

	sched = march.make_service_sched("Simplified", [1, [39]], None)
	mongo_io = march.make_serv_inst(servName = "mongo_io", servDomain = "", instName = "mongo_io",
	 modelName = "mongo_io", sched = sched, machId = 17)

	services = [nginx, unique_id, url_shorten, media, text, user_tag, recommend, read_home_t, compose_post, user_timeline, write_home_timeline, user, social_graph, post_storage, rabbit_mq, memcached, mongodb, mongo_io]

	edges = []

	edges.append(march.make_edge(src = "nginx", targ = "unique_id", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "url_shorten", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "media", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "text", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "user_tag", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "recommend", bidir = True))
	edges.append(march.make_edge(src = "user", targ = "recommend", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "read_home_t", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "compose_post", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "social_graph", bidir = True))
	edges.append(march.make_edge(src = "nginx", targ = "post_storage", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "unique_id", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "url_shorten", bidir = True))
	edges.append(march.make_edge(src = "read_home_t", targ = "url_shorten", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "media", bidir = True))
	edges.append(march.make_edge(src = "post_storage", targ = "media", bidir = True))
	edges.append(march.make_edge(src = "memcached", targ = "media", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "text", bidir = True))
	edges.append(march.make_edge(src = "user", targ = "text", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "user_tag", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "user", bidir = True))
	edges.append(march.make_edge(src = "read_home_t", targ = "post_storage", bidir = True))
	edges.append(march.make_edge(src = "read_home_t", targ = "memcached", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "post_storage", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "user_timeline", bidir = True))
	edges.append(march.make_edge(src = "compose_post", targ = "rabbit_mq", bidir = True))
	edges.append(march.make_edge(src = "user", targ = "mongodb", bidir = True))
	edges.append(march.make_edge(src = "user", targ = "memcached", bidir = True))
	edges.append(march.make_edge(src = "social_graph", targ = "user", bidir = True))
	edges.append(march.make_edge(src = "social_graph", targ = "mongodb", bidir = True))
	edges.append(march.make_edge(src = "social_graph", targ = "memcached", bidir = True))
	edges.append(march.make_edge(src = "post_storage", targ = "mongodb", bidir = True))
	edges.append(march.make_edge(src = "post_storage", targ = "memcached", bidir = True))
	edges.append(march.make_edge(src = "user_timeline", targ = "post_storage", bidir = True))
	edges.append(march.make_edge(src = "user_timeline", targ = "mongodb", bidir = True))
	edges.append(march.make_edge(src = "user_timeline", targ = "memcached", bidir = True))
	edges.append(march.make_edge(src = "rabbit_mq", targ = "write_home_timeline", bidir = True))
	edges.append(march.make_edge(src = "rabbit_mq", targ = "memcached", bidir = True))
	edges.append(march.make_edge(src = "write_home_timeline", targ = "memcached", bidir = True))


	graph = march.make_cluster(services = services, edges = edges, netLat = 65000)

	with open("./json/graph.json", "w+") as f:
		json.dump(graph, f, indent=2)

if __name__ == "__main__":
	main()

