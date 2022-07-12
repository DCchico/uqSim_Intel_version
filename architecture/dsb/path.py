from asyncio import FastChildWatcher
from curses import noecho
import sys
import os
import json
import make_arch as march 


def main():
	# path 0: Compose Post path
	nodeList = []

	node = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 0, needSync = False, syncNodeId = None, childs = [1])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "compose_post", servDomain = "", codePath = 0, startStage = 0, endStage = 1, 
		nodeId = 1, needSync = True, syncNodeId = 10, childs = [2,5,6,7,8,9,10])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "user", servDomain = "", codePath = 0, startStage = 0, endStage = 1, 
		nodeId = 2, needSync = True,  syncNodeId = 5, childs = [3,4])
	nodeList.append(node)	

	node = march.make_serv_path_node(servName = "recommend", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 3, needSync = False,  syncNodeId = None, childs = [5])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "social_graph", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 4, needSync = False, syncNodeId = None, childs = [5])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "user", servDomain = "", codePath = 0, startStage = 1, endStage = -1, 
		nodeId = 5, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "unique_id", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 6, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "url_shorten", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 7, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "media", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 8, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "text", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 9, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "user_tag", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 10, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "read_home_t", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 11, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "compose_post", servDomain = "", codePath = 0, startStage = 2, endStage = -1, 
		nodeId = 12, needSync = False, syncNodeId = None, childs = [13])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "user_timeline", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 11, needSync = False,  syncNodeId = None, childs = [12])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "post_storage", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 12, needSync = False,  syncNodeId = None, childs = [13])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "rabbit_mq", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 13, needSync = False,  syncNodeId = None, childs = [14])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "write_home_timeline", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 14, needSync = False,  syncNodeId = None, childs = [15])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "memcached", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 15, needSync = False,  syncNodeId = None, childs = [16])
	nodeList.append(node)

	node = march.make_serv_path_node(servName = "client", servDomain = "", codePath = -1, startStage = 0, endStage = -1, 
		nodeId = 16, needSync = False, syncNodeId = None, childs = [])
	nodeList.append(node)

	path_memc_hit = march.make_serv_path(pathId = 0, entry = 0, prob = 86, nodes = nodeList)

	'''
	# path 1: memcached miss mongo hit
	base_node_id = 4
	nodeList = []
	node_0 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 0 + base_node_id, needSync = False, syncNodeId = None, childs = [1 + base_node_id])
	nodeList.append(node_0)

	node_1 = march.make_serv_path_node(servName = "memcached", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 1 + base_node_id, needSync = False, syncNodeId = None, childs = [2 + base_node_id])
	nodeList.append(node_1)

	# should be a different nginx path
	node_2 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 2 + base_node_id, needSync = False, syncNodeId = None, childs = [3 + base_node_id])
	nodeList.append(node_2)

	node_3 = march.make_serv_path_node(servName = "mongodb", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 3 + base_node_id, needSync = False, syncNodeId = None, childs = [4 + base_node_id])
	nodeList.append(node_3)

	node_4 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 4 + base_node_id, needSync = False, syncNodeId = None, childs = [5 + base_node_id])
	nodeList.append(node_4)

	node_5 = march.make_serv_path_node(servName = "memcached", servDomain = "", codePath = 1, startStage = 0, endStage = -1, 
		nodeId = 5 + base_node_id, needSync = False, syncNodeId = None, childs = [6 + base_node_id])
	nodeList.append(node_5)

	node_6 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 6 + base_node_id, needSync = False, syncNodeId = None, childs = [7 + base_node_id])
	nodeList.append(node_6)

	node_7 = march.make_serv_path_node(servName = "client", servDomain = "", codePath = -1, startStage = 0, endStage = -1, 
		nodeId = 7 + base_node_id, needSync = False, syncNodeId = None, childs = [])
	nodeList.append(node_7)

	path_memc_miss_mongo_hit = march.make_serv_path(pathId = 1, entry = base_node_id, prob = 12, nodes = nodeList)


	base_node_id = 12

	# path 2: memcached miss mongo miss
	nodeList = []
	node_0 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 0 + base_node_id, needSync = False, syncNodeId = None, childs = [1 + base_node_id])
	nodeList.append(node_0)

	node_1 = march.make_serv_path_node(servName = "memcached", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 1 + base_node_id, needSync = False, syncNodeId = None, childs = [2 + base_node_id])
	nodeList.append(node_1)

	# should be a different nginx path
	node_2 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 2 + base_node_id, needSync = False, syncNodeId = None, childs = [3 + base_node_id])
	nodeList.append(node_2)

	node_3 = march.make_serv_path_node(servName = "mongodb", servDomain = "", codePath = 1, startStage = 0, endStage = 1, 
		nodeId = 3 + base_node_id, needSync = True, syncNodeId = 5 + base_node_id, childs = [4 + base_node_id])
	nodeList.append(node_3)

	node_4 = march.make_serv_path_node(servName = "mongo_io", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 4 + base_node_id, needSync = False, syncNodeId = None, childs = [5 + base_node_id])
	nodeList.append(node_4)

	node_5 = march.make_serv_path_node(servName = "mongodb", servDomain = "", codePath = 1, startStage = 2, endStage = -1, 
		nodeId = 5 + base_node_id, needSync = False, syncNodeId = None, childs = [6 + base_node_id])
	nodeList.append(node_5)

	node_6 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 6 + base_node_id, needSync = False, syncNodeId = None, childs = [7 + base_node_id])
	nodeList.append(node_6)

	node_7 = march.make_serv_path_node(servName = "memcached", servDomain = "", codePath = 1, startStage = 0, endStage = -1, 
		nodeId = 7 + base_node_id, needSync = False, syncNodeId = None, childs = [8 + base_node_id])
	nodeList.append(node_7)

	node_8 = march.make_serv_path_node(servName = "nginx", servDomain = "", codePath = 0, startStage = 0, endStage = -1, 
		nodeId = 8 + base_node_id, needSync = False, syncNodeId = None, childs = [9 + base_node_id])
	nodeList.append(node_8)

	node_9 = march.make_serv_path_node(servName = "client", servDomain = "", codePath = -1, startStage = 0, endStage = -1, 
		nodeId = 9 + base_node_id, needSync = False, syncNodeId = None, childs = [])
	nodeList.append(node_9)

	path_memc_miss_mongo_miss = march.make_serv_path(pathId = 2, entry = base_node_id, prob = 2, nodes = nodeList)
	'''


	#paths = [path_memc_hit, path_memc_miss_mongo_hit, path_memc_miss_mongo_miss]
	paths = [path_memc_hit]


	with open("./json/path.json", "w+") as f:
		json.dump(paths, f, indent=2)

if __name__ == "__main__":
	main()