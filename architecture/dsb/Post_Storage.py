import sys
import os
import json
import make_arch as march 

# post_storage Microservice
def main():
	# req path
	
	recvTm = march.make_time_model("expo", [1500])
	respTm = None
	epoll_stage = march.make_stage(stage_name = "epoll", pathId = 0, pathStageId = 0, stageId = 0, blocking = False, batching = True, socket = False, 
		epoll = True, ngx = False,  net = False, chunk = False, recvTm = recvTm, respTm = respTm, cm = None, criSec = False, threadLimit = None, 
		scaleFactor = 0.55)

	recvTm = march.make_time_model("expo", [19000])
	respTm = None
	proc_stage = march.make_stage(stage_name = "proc", pathId = 0, pathStageId = 1, stageId = 1, blocking = False, batching = False, socket = False, 
		epoll = False, ngx = False,  net = True, chunk = False, recvTm = recvTm, respTm = respTm, cm = None, criSec = False, threadLimit = None, 
		scaleFactor = 0.4)

	req_path = march.make_code_path(pathId = 0, prob = 100, stages= [epoll_stage, proc_stage], priority = None)

	# resp path

	recvTm = march.make_time_model("expo", [19000])
	respTm = None
	proc_resp_stage = march.make_stage(stage_name = "proc_resp", pathId = 0, pathStageId = 1, stageId = 1, blocking = False, batching = False, socket = False, 
		epoll = False, ngx = True,  net = True, chunk = False, recvTm = recvTm, respTm = respTm, cm = None, criSec = False, threadLimit = None, 
		scaleFactor = 1.0)

	resp_path = march.make_code_path(pathId = 1, prob = None, stages=[proc_resp_stage], priority = None)

	# post_storage
	comp = march.make_micro_service(servType = "micro_service", servName = "post_storage", bindConn = True, paths = [req_path], 
		baseFreq = 2600, curFreq = 2600)

	with open("./json/microservice/post_storage.json", "w+") as f:
		json.dump(comp, f, indent=2)


if __name__ == "__main__":
	main();

