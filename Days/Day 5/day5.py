test_lines = [
"seeds: 79 14 55 13",
"\n",
"seed-to-soil map:",
"50 98 2",
"52 50 48",
"\n",
"soil-to-fertilizer map:",
"0 15 37",
"37 52 2",
"39 0 15",
"\n",
"fertilizer-to-water map:",
"49 53 8",
"0 11 42",
"42 0 7",
"57 7 4",
"\n",
"water-to-light map:",
"88 18 7",
"18 25 70",
"\n",
"light-to-temperature map:",
"45 77 23",
"81 45 19",
"68 64 13",
"\n",
"temperature-to-humidity map:",
"0 69 1",
"1 0 69",
"\n",
"humidity-to-location map:",
"60 56 37",
"56 93 4"
]

map_lines=dict()
curr_map=""
for line in test_lines:
    if line=="\n":
        continue
    if ":" in line:
        if "seeds" in line:
            curr_map="seeds"
            map_lines[curr_map] = line.split(": ")[1]
        elif "seed-to-soil" in line:
            curr_map = "seed-to-soil"
        elif "soil-to-fertilizer" in line:
            curr_map = "soil-to-fertilizer"
        elif "fertilizer-to-water" in line:
            curr_map = "fertilizer-to-water"
        elif "water-to-light" in line:
            curr_map = "water-to-light"
        elif "light-to-temperature" in line:
            curr_map = "light-to-temperature"
        elif "temperature-to-humidity" in line:
            curr_map = "temperature-to-humidity"
        elif "humidity-to-location" in line:
            curr_map = "humidity-to-location"
    else:
        curr_map_lines_arr = map_lines.get(curr_map,[])
        curr_map_lines_arr.append(line)
        map_lines[curr_map]= curr_map_lines_arr
        
seeds = map_lines["seeds"].split(" ")

seed_arr=[]
for i in range(0,len(seeds),2):
    seed_arr.append([seeds[i],seeds[i+1]])
seed_arr

big_map=dict()
for key in map_lines.keys():
    if key =="seeds":
        continue
    else:
        curr_map_lines = map_lines[key]
        big_map[key] = []
        for line in curr_map_lines:
            dest_start,source_start,range_len = line.split(" ")
            range_len = range_len.replace("\n","")
            curr_array = big_map[key]
            curr_array.append([dest_start,source_start,range_len ])
            big_map[key] = curr_array

def temp_dest(input_start,input_range_len,lines):
    output_temp_arr=[]
    input_start = int(input_start)
    input_range_len = int(input_range_len)
    for line in lines:
        #print(line)
        dest_range_start,source_range_start,range_len = line
        dest_range_start = int(dest_range_start)
        source_range_start = int(source_range_start)
        range_len = int(range_len)
        if (input_start >= source_range_start) and (input_start<=source_range_start+range_len):
            # if input_start inside of source start and source end range
            if input_start+input_range_len<=source_range_start+range_len:
                # if input range wholly inside the source start and end range
                print("case1")
                dest_mapped_start = dest_range_start+input_start-source_range_start
                dest_mapped_end = dest_range_start+input_start-source_range_start+input_range_len
                input_start_curr = input_start
                input_end_curr = input_start+input_range_len
                output_temp_arr.append([input_start_curr,input_end_curr,dest_mapped_start,dest_mapped_end])
            else:
                # if input range goes past the end of the source end location 
                print("case2")
                print(line)
                dest_mapped_start = dest_range_start+input_start-source_range_start
                dest_mapped_end = dest_range_start+range_len
                input_start_curr = input_start
                input_end_curr = source_range_start+range_len
                output_temp_arr.append([input_start_curr,input_end_curr,dest_mapped_start,dest_mapped_end])
                # Recursively call function that returns output_temp_arr lines for the rest of the range
                rest_of_range_list = temp_dest(source_range_start+range_len+1,input_start+input_range_len-(source_range_start+range_len+1),lines)
                for vals in rest_of_range_list:
                    output_temp_arr.append(vals)
                    
        elif (input_start + input_range_len>= source_range_start) and (input_start+ input_range_len<=source_range_start+range_len):
            # if input end is inside of source start and source end range
            # dest start and input end will be used
            print("case3")
            dest_mapped_start = dest_range_start
            dest_mapped_end = dest_range_start+input_start-source_range_start+input_range_len
            input_start_curr = source_range_start
            input_end_curr = input_start+input_range_len
            output_temp_arr.append([input_start_curr,input_end_curr,dest_mapped_start,dest_mapped_end])
            # Get mapping for input start to source range start:
            print(input_start,source_range_start,input_start+ input_range_len,source_range_start+range_len)
            print(source_range_start,input_start+input_range_len-source_range_start)
            rest_of_range_list = temp_dest(input_start,source_range_start-input_start-1,lines)
            for vals in rest_of_range_list:
                output_temp_arr.append(vals)

        elif (input_start <= source_range_start) and (input_start+ input_range_len>=source_range_start+range_len):
            # if input range wholly contains the source range
            print("case4")
            dest_mapped_start = dest_range_start
            dest_mapped_end = dest_range_start+range_len
            input_start_curr = source_range_start
            input_end_curr = source_range_start+range_len
            output_temp_arr.append([input_start_curr,input_end_curr,dest_mapped_start,dest_mapped_end])
            # Get mapping for Before section:
            rest_of_range_list = temp_dest(input_start,source_range_start-input_start-1,lines)
            for vals in rest_of_range_list:
                output_temp_arr.append(vals)
            # Get mapping for After Section:
            rest_of_range_list = temp_dest(source_range_start+range_len+1,input_start+input_range_len-(source_range_start+range_len+1),lines)
            for vals in rest_of_range_list:
                output_temp_arr.append(vals)
    if len(output_temp_arr) ==0:
        #handle no match cases
        print("case5")
        output_temp_arr.append([input_start,input_start+input_range_len,input_start,input_start+input_range_len])
    return output_temp_arr

def find_dest(input_start,input_range_len,lines):
    output_temp_arr = temp_dest(input_start,input_range_len,lines)

    #need to catch any sequences in the input range that did not match to an output 
    output_arr = []
    print("Temp Output",output_temp_arr)
    for input_start_curr,input_end_curr,dest_mapped_start,dest_mapped_end in output_temp_arr:
        output_arr.append([dest_mapped_start,dest_mapped_end-dest_mapped_start])
    
    return output_arr

def range_lists_to_output_range_lists(range_lists,map_key):
    output_range_lists =[]
    for range_start,range_len in range_lists:
        output = find_dest(range_start,range_len,big_map[map_key])
        for output_start,output_range_len in output:
            output_range_lists.append([output_start,output_range_len])
    return output_range_lists

def seed_to_location(seed,seed_range_len):
    print("INPUT:",f"[{seed},{seed_range_len}]")
    soil_range_lists = find_dest(seed,seed_range_len,big_map["seed-to-soil"])
    print("SOIL:",soil_range_lists)
    fertilizer_range_lists = range_lists_to_output_range_lists(soil_range_lists,'soil-to-fertilizer')
    print("FERTILIZER:",fertilizer_range_lists)
    water_range_lists = range_lists_to_output_range_lists(fertilizer_range_lists,'fertilizer-to-water')
    print("WATER:",water_range_lists)
    light_range_lists = range_lists_to_output_range_lists(water_range_lists,'water-to-light')
    print("LIGHT:",light_range_lists)
    tempurature_range_lists = range_lists_to_output_range_lists(light_range_lists,'light-to-temperature')
    print("TEMPERATURE:",tempurature_range_lists)
    humidity_range_lists = range_lists_to_output_range_lists(tempurature_range_lists,'temperature-to-humidity')
    print("HUMIDITY:",humidity_range_lists)
    location_range_lists = range_lists_to_output_range_lists(humidity_range_lists,'humidity-to-location')
    print("LOCATION:",location_range_lists)
    return location_range_lists 

location_arr = []
for seed_start,seed_range_len in seed_arr:
    location = seed_to_location(seed_start,seed_range_len)
    print(int(seed_start),",",int(seed_range_len),"->",location)
    location_arr.append(location)
print(location)
final_loc_array=[]
for elem in location_arr:
    for start,range_len in elem:
        final_loc_array.append(start)
print(min(final_loc_array))