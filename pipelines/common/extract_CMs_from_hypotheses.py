#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import json

SSforS = {
'ANIMAL': 'ACTION', 
'BODY_OF_WATER': 'MOVEMENT', 
'CONFINEMENT': 'EXIT',
'ENSLAVEMENT': 'OPRESSION',
'MAZE': 'OBSTRUCTION',
'PARASITE': 'DESTRUCTUVE_BEING',
'PHYSICAL_BURDEN': 'RELIEF',
'PHYSICAL_LOCATION': 'DEFINED_REGION',
'DARKNESS': 'DARK_END_OF_RANGE_OF_DARKNESS/LIGHT',
'LOW_POINT': 'MOVEMENT_DOWNWARD',
'BUILDING': 'CREATION_DESTRUCTION',
'MEDICINE': 'ADMINISTRATION',
'MORAL_DUTY': 'REMUNERATION',
'VERTICAL_SCALE': 'MOVEMENT_ON_THE_SCALE',
'DESTROYER': 'DESTRUCTIVE_FORCE',
'ENABLER': 'LUBRICANT',
'OBESITY': 'EXCESS_CONSUMPTION',
'RESOURCE': 'QUANTITY_SIZE',
'VISION': 'SEEING',
'HIGH_POINT': 'TOP_OF_ECONOMIC_SCALE',
'LIGHT': 'LIGHT_END_OF_RANGE_OF_DARKNESS/LIGHT',
'BLOOD_SYSTEM': 'MOVEMENT',
'CROP': 'PLANTING',
'MOVEMENT': 'MOVEMENT',
'FOOD': 'CONSUMPTION',
'GAME': 'ACTIONS',
'PLANT': 'CHANGE_OF_STATE'}

def wordStr2print(Args,WordProps,Equalities):
	output_str = ''

	for arg in Args:
		newwords = findWords(arg,WordProps,Equalities,False)
		if len(newwords)>0:	output_str += ',' + findWords(arg,WordProps,Equalities,False)
	
	return output_str[1:]

def wordStr2print_Mapping(labeledProps,WordProps,Equalities):
	output_str = ''
	for (propName,args) in labeledProps:
		output_str += ', ' + propName + '['
		words_str = ''
		for arg in args:			
			words = findWords(arg,WordProps,Equalities,True)
			words_str += '; ' + words
		if len(words_str)>0:	
			words_str = words_str[2:]

		output_str += words_str + ']' 

	#print json.dumps(output_str[2:], ensure_ascii=False)
	return output_str[2:]

def findWords(ARG,WordProps,Equalities,isMapping):
	all_args = []
	if isMapping and Equalities.has_key(ARG): all_args = Equalities[ARG].keys()

	all_args.append(ARG)

	output_str = ''
	for arg in all_args:
		if not arg.startswith('_') and not arg.startswith('u'):
			for (propName,args) in WordProps:
				if arg == args[0] and (propName.endswith('-vb') or propName.endswith('-rb') or propName.endswith('-adj') or propName.endswith('-nn')):
					if propName.endswith('-adj'): output_str += ',' + propName[:-4]
					else: output_str += ',' + propName[:-3]
				elif len(args)>1 and arg ==args[1] :
					if propName.endswith('-nn'): output_str += ',' + propName[:-3]
					elif propName=='person': output_str += ',person'
				#TODO: enable when Boxer starts working correctly
				#elif propName=='subset-of' and arg==args[2] :
				#	output_str += ',' + findWords(args[1],WordProps,Equalities,isMapping)
	
	if len(output_str)>0: 
		return output_str[1:]

	if isMapping:	return ARG		
	return ''

def createDStruc(superD,subD):
	outputstrucs = defaultdict(dict)

	for superd in superD:
		for superArgs in superD[superd]:
			if not outputstrucs.has_key(superd) or not outputstrucs[superd].has_key(superArgs[0]): outputstrucs[superd][superArgs[0]] = []
			for subd in subD:
				for subArgs in subD[subd]:
					if len(subArgs)>1 and superArgs[0]==subArgs[1]:
						outputstrucs[superd][superArgs[0]].append((subd,subArgs[0]))

	#print json.dumps(outputstrucs, ensure_ascii=False)
	return outputstrucs

def collectVars(struc,superkey,equalities):
	output = []

	for arg in struc[superkey]:
		if not arg.startswith('_'): 
			output.append(arg)
			if equalities.has_key(arg):
				for a in equalities[arg]: output.append(a)
		for (subd,subarg) in struc[superkey][arg]:
			if not subarg.startswith('_'): 
				output.append(subarg)
				if equalities.has_key(subarg):
					for a in equalities[subarg]: output.append(a)
	return output

def isLinkedbyParse(v1,v2,word_props,equalities,been):
	if (v1,v2) in been: return 0
	been.append((v1,v2))
	been.append((v2,v1))

	#if equalities.has_key(v1) and equalities[v1].has_key(v2): return 2

	for (propName,args) in word_props:
		if v1 in args and v2 in args: return 2

	for (propName,args) in word_props:
		if v1 in args:
			if len(args)>2: 
				i1 = args.index(v1)
				if i1==0: 
					if isLinkedbyParse(args[1],v2,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[2],v2,word_props,equalities,been)>0: return 1
					if len(args)>3 and isLinkedbyParse(args[3],v2,word_props,equalities,been)>0: return 1
				elif i1==1:
					if isLinkedbyParse(args[0],v2,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[2],v2,word_props,equalities,been)>0: return 1
					if len(args)>3 and isLinkedbyParse(args[3],v2,word_props,equalities,been)>0: return 1
				elif i1==2:
					if isLinkedbyParse(args[0],v2,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[1],v2,word_props,equalities,been)>0: return 1
					if len(args)>3 and isLinkedbyParse(args[3],v2,word_props,equalities,been)>0: return 1
				elif i1==3:
					if isLinkedbyParse(args[0],v2,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[1],v2,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[2],v2,word_props,equalities,been)>0: return 1
		elif v2 in args:
			if len(args)>2: 
				i2 = args.index(v2)
				if i2==0: 
					if isLinkedbyParse(args[1],v1,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[2],v1,word_props,equalities,been)>0: return 1
					if len(args)>3 and isLinkedbyParse(args[3],v1,word_props,equalities,been)>0: return 1
				elif i2==1:
					if isLinkedbyParse(args[0],v1,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[2],v1,word_props,equalities,been)>0: return 1
					if len(args)>3 and isLinkedbyParse(args[3],v1,word_props,equalities,been)>0: return 1
				elif i2==2:
					if isLinkedbyParse(args[0],v1,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[1],v1,word_props,equalities,been)>0: return 1
					if len(args)>3 and isLinkedbyParse(args[3],v1,word_props,equalities,been)>0: return 1
				elif i2==3:
					if isLinkedbyParse(args[0],v1,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[1],v1,word_props,equalities,been)>0: return 1
					if isLinkedbyParse(args[2],v1,word_props,equalities,been)>0: return 1

	return 0

def extract_CM_mapping(id,inputString,DESCRIPTION,LCCannotation):
	targets = dict()	
	subtargets = dict()
	subsubtargets = dict()
	sources = dict()
	subsources = dict()
	mappings = []
	roles = []
	word_props = []
	equalities = defaultdict(dict)

	sourceTask = False
	if LCCannotation:
		if "sourceFrame" in LCCannotation and "targetFrame" in LCCannotation and "targetConceptSubDomain" in LCCannotation:
			if LCCannotation["sourceFrame"] and len(LCCannotation["sourceFrame"])>0:
				if LCCannotation["targetFrame"] and len(LCCannotation["targetFrame"])>0:
					if LCCannotation["targetConceptSubDomain"] and len(LCCannotation["targetConceptSubDomain"])>0:
						sourceTask = True

	prop_pattern = re.compile('([^\(]+)\(([^\)]+)\)')
	
	propositions = inputString.split(' ^ ')
	prop_list = []
	for item in propositions:
		prop_match_obj = prop_pattern.match(item)
		if prop_match_obj:
			prop_name = prop_match_obj.group(1)
			arg_str = prop_match_obj.group(2)
			args = arg_str.split(',')

			if prop_name.startswith('T#'):
				if not targets.has_key(prop_name[2:]): targets[prop_name[2:]] = []
				targets[prop_name[2:]].append(args)
			elif prop_name.startswith('TS#'):
				dname = prop_name[3:]
				if not sourceTask or dname == LCCannotation["targetFrame"]:
					if not subtargets.has_key(dname): subtargets[dname] = []
					subtargets[dname].append(args)
			elif prop_name.startswith('TSS#'):
				dname = prop_name[4:]
				if not sourceTask or dname == LCCannotation["targetConceptSubDomain"]:
					if not subsubtargets.has_key(dname): subsubtargets[dname] = []
					subsubtargets[dname].append(args)
			elif prop_name.startswith('S#'):
				dname = prop_name[2:]
				if not sourceTask or dname == LCCannotation["sourceFrame"]:
					if not sources.has_key(dname): sources[dname] = []
					sources[dname].append(args)
			elif prop_name.startswith('SS#'):
				if not subsources.has_key(prop_name[3:]): subsources[prop_name[3:]] = []
				subsources[prop_name[3:]].append(args)
			elif prop_name.startswith('M#'):
				mappings.append((prop_name[2:],args))
			elif prop_name.startswith('R#'):
				pass
			elif prop_name.startswith('I#'):
				pass
			elif prop_name == '=':
				for i in range(len(args)):
					arg1 = args[i]
					j = i + 1
					while j < len(args):
						arg2 = args[j]  
						equalities[arg1][arg2]=1
						equalities[arg2][arg1]=1
						j += 1
			else:
				#print json.dumps((prop_name,args), ensure_ascii=False) 
				if prop_name == 'equal':
					equalities[args[1]][args[2]]=1
					equalities[args[2]][args[1]]=1
				else: word_props.append((prop_name,args))

	#print json.dumps(targets, ensure_ascii=False)

	for el1 in equalities.keys():
		for el2 in equalities[el1].keys():
			for el3 in equalities[el2].keys():
				if el1 != el3:
					equalities[el1][el3]=1
					equalities[el3][el1]=1

	target_strucs = createDStruc(subtargets,subsubtargets)
	source_strucs = createDStruc(sources,subsources)

	#print json.dumps(target_strucs, ensure_ascii=False)
	#print json.dumps(source_strucs, ensure_ascii=False)
	#print json.dumps(equalities, ensure_ascii=False)

	output_struct_item = {}
	if not LCCannotation: output_struct_item["id"] = id
	output_struct_item["isiDescription"] = DESCRIPTION
	output_struct_item["targetConceptDomain"] = "ECONOMIC_INEQUALITY"

	explanationAppendix = "\n%%BEGIN_CM_LIST\n"


	CMlinked = ''
	CMhalflinked = ''
	CMunlinked = ''

	for targetS in target_strucs:
		tV = collectVars(target_strucs,targetS,equalities)

		Tstrings = []
		for targ in target_strucs[targetS]: 
			if len(target_strucs[targetS][targ])==0: 
				Tstrings.append('ECONOMIC_INEQUALITY,' + targetS + ',' + targetS)
			else: 		
				for (tsubd,tsubarg) in target_strucs[targetS][targ]:
					Tstrings.append('ECONOMIC_INEQUALITY,' + targetS + ',' + tsubd)

		for sourceS in source_strucs:
			sV = collectVars(source_strucs,sourceS,equalities)
			link = 0
			for tv in tV:
				for sv in sV:
					newlink = isLinkedbyParse(tv,sv,word_props,equalities,[])
					if newlink==2:
						link = 2
						break
					elif newlink>link: link=newlink
				if link==2: break

			if sourceS == 'SCHISM':
				Tstrings.append('ECONOMIC_INEQUALITY,POVERTY/WEALTH,POVERTY/WEALTH')

			Sstrings = []
			for sarg in source_strucs[sourceS]:
				if len(source_strucs[sourceS][sarg])==0:
					if SSforS.has_key(sourceS): 
						Sstrings.append(','+sourceS+','+SSforS[sourceS])
					else: Sstrings.append(','+sourceS+',TYPE')				
				else:
					for (ssubd,ssubarg) in source_strucs[sourceS][sarg]:
						Sstrings.append(','+sourceS+','+ssubd)

			for ts in Tstrings:
				for ss in Sstrings:
					explanationAppendix += ts+ss
					if link==2: 
						explanationAppendix += ',0.9\n'
						CMlinked = ts+ss
					elif link==1: 
						explanationAppendix += ',0.5\n'
						CMhalflinked = ts+ss
					elif link==0: 
						explanationAppendix += ',0.3\n'
						CMunlinked = ts+ss

	if len(CMlinked)==0 and len(CMhalflinked)==0 and len(CMunlinked)==0:
		targetS = ''
		sourceS = ''

		if len(target_strucs.keys())>0:
			guessTarget = target_strucs.keys()[0]
			tArg = target_strucs[guessTarget].keys()[0]
			if len(target_strucs[guessTarget][tArg])>0:
				(guessSubTarget,stArg) = target_strucs[guessTarget][tArg][0]
			else: guessSubTarget = guessTarget
			targetS = 'ECONOMIC_INEQUALITY,' + guessTarget + ',' + guessSubTarget + ','
		else:
			if sourceTask:
				guessTarget = LCCannotation["targetFrame"]
				guessSubTarget = LCCannotation["targetConceptSubDomain"]
			else:
				guessTarget = 'POVERTY'
				guessSubTarget = 'POVERTY'
			targetS = 'ECONOMIC_INEQUALITY,' + guessTarget + ',' + guessSubTarget + ','

		#print json.dumps(source_strucs, ensure_ascii=False)
		if len(source_strucs.keys())>0:
			guessSource = source_strucs.keys()[0]
			sArg = source_strucs[guessSource].keys()[0]
			if len(source_strucs[guessSource][sArg])>0:
				(guessSubSource,stArg) = source_strucs[guessSource][sArg][0]
			else: 
				if SSforS.has_key(guessSource): guessSubSource = SSforS[guessSource]
				else: guessSubSource = 'TYPE'
			sourceS = guessSource + ',' + guessSubSource
		else:
			if sourceTask:
				guessSource = LCCannotation["sourceFrame"]
			else:
				guessSource = 'STRUGGLE'
			if SSforS.has_key(guessSource): guessSubSource = SSforS[guessSource]
			else: guessSubSource = 'TYPE'
			sourceS = guessSource + ',' + guessSubSource

			if guessSource == 'SCHISM':
				targetS = 'ECONOMIC_INEQUALITY,POVERTY/WEALTH,POVERTY/WEALTH,'

		CMunlinked = targetS+sourceS
		explanationAppendix += targetS+sourceS+',0.001\n'

	if len(CMlinked)>0: bestCM = CMlinked
	elif len(CMhalflinked)>0: bestCM = CMhalflinked
	else: bestCM = CMunlinked

	explanationAppendix += "%%END_CM_LIST"

	output_struct_item['isiAbductiveExplanation'] = inputString + explanationAppendix.encode("utf-8")
	output_struct_item["targetConceptDomain"] = 'ECONOMIC_INEQUALITY'
	data = bestCM.split(',')
	output_struct_item["targetFrame"] = data[1]
	output_struct_item["targetConceptSubDomain"] = data[2]
	output_struct_item["sourceFrame"] = data[3]
	if data[4]=='-': output_struct_item["sourceConceptSubDomain"] = 'TYPE'
	else: output_struct_item["sourceConceptSubDomain"] = data[4]

	targetArgs = dict()
	if subtargets.has_key(data[1]):
		for args in subtargets[data[1]]:
			targetArgs[args[0]]=1
	if subsubtargets.has_key(data[2]):
		for args in subsubtargets[data[2]]:
			targetArgs[args[0]]=1

	sourceArgs = dict()
	if sources.has_key(data[3]):
		for args in sources[data[3]]:
			sourceArgs[args[0]]=1
	if subsources.has_key(data[4]):
		for args in subsources[data[4]]:
			sourceArgs[args[0]]=1

	targetWords = wordStr2print(targetArgs,word_props,equalities)
	sourceWords = wordStr2print(sourceArgs,word_props,equalities)

	mapping_str = wordStr2print_Mapping(mappings,word_props,equalities)

	annotationMappings_struc = dict()
	annotationMappings_struc['explanation'] = mapping_str
	annotationMappings_struc['target'] = targetWords
	annotationMappings_struc['source'] = sourceWords
	if len(targetWords)>0: annotationMappings_struc['targetInLm'] = True
	else: annotationMappings_struc['targetInLm'] = False
	if len(sourceWords)>0: annotationMappings_struc['sourceInLm'] = True
	else: annotationMappings_struc['sourceInLm'] = False

	output_struct_item['annotationMappings'] = [annotationMappings_struc]

	#print json.dumps(output_struct_item, ensure_ascii=False)

	return output_struct_item
