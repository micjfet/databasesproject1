from collections import Counter
from itertools import combinations
from itertools import product
#Michael Fetter, RDBMS normalizer for CS5300
#make it so that if 1nf in a fd, it decomposes based on the fd instead of primary key - maybe

#main function to gather necessary inputs, call normalization process, and output normalized tables
def input_parser():
    #loop to continue accepting new relations to normalize until the user inputs that they are done with the program
    while True:
        #asks the user if they want to input another relation (also asks when the user first starts the program)
        new_relation_exists = 'NULL'
        while new_relation_exists != 'y' and new_relation_exists != 'n':
            print("Would you like to input a relation? (y/n)")
            new_relation_exists = input()
            if new_relation_exists != 'y' and new_relation_exists != 'n':
                print("Invalid input")
        if new_relation_exists == 'n':
            break
        
        #asks user for table name and its attributes as inputs 
        tables = {}
        table_name = input("What do you want to name the table?\n")
        attributes = []
        print("\nAdd attributes in form a1,a2,a3,a4")
        current_attribute = input()
        attributes = list(current_attribute.split(","))
        
        #creates an initial table in the dictionary
        tables[table_name] = {
            'attributes': attributes,
            'cand_keys': [],
            'multi-valued_attributes': [],
            'left_fds': [],
            'right_fds': []
        }

        #adds candidate keys based on user inputs
        cand_keys = []
        if attributes:
            print("\nEach candidate key can be made of one or more attributes.")
            print("Enter primary keys in form a1,a2 a3 (this would give you two keys: (a1,a2) and (a3))")
            print(f"Available attributes: {attributes}")
            
            #loop to collect inputs until user inputs a valid key
            while True:
                cand_keys = []
                validkey = True
                keys = input()
                keys = keys.split(" ")
                for current_key in keys:
                    current_key = current_key.split(",")
                    cand_keys.append(current_key)
                    for k in current_key:
                        if k not in attributes:
                            validkey = False
                if validkey == True:
                    break
                else:
                    print("Invalid candidate key was entered, please enter only valid candidate keys")

            #adds multi-valued-attributes based on inputs given by users
            multi_valued_attributes = []
            multi_value_exist = input("\nAre there any non-atomic attributes? (y/n)\n").lower()
            if multi_value_exist == 'y':
                print("\nEnter any multi-valued (non-atomic) attributes in the relation in form a1,a2")
                print(f"Available attributes: {attributes}")
                
                #loop to collect inputs until user inputs a valid set of multi-valued-attributes
                while True:
                    valid_mv = True
                    multi_valued_attributes = input()
                    multi_valued_attributes = list(multi_valued_attributes.split(","))
                    for mv in multi_valued_attributes:
                        if mv not in attributes:
                            valid_mv = False
                    if valid_mv == True:
                        break
                    else:
                        print(f"Invalid multi-valued attribute was entered, please enter only valid multi-valued attributes")
        
            #adds functional dependencies based on inputs in expected form from user
            functional_dependencies_exist = input("\nDo you want to add functional dependencies? (y/n)\n")
            if functional_dependencies_exist == 'y':
                left_fds = []
                right_fds = []
                
                #loops until user inputs valid set of functional dependencies
                while True: 
                    print("\nEnter functional dependencies in form a1,a2->a3,a4 a5->a6 on a single line")
                    print(f"Available attributes: {attributes}")
                    fd_string = input()
                    fd_string = fd_string.split(" ")
                    fd_num = 0
                    valid_fd = True
                    for fd in fd_string:
                        if "->" not in fd:
                            valid_fd = False
                        fd = fd.split("->")
                        fd_string[fd_num] = fd
                        fd_num += 1
                        a_num = 0
                        for a in fd:
                            a = a.split(",")
                            fd[a_num] = a
                            a_num += 1
                            for piece in a:
                                if piece not in attributes:
                                    valid_fd = False
                    if valid_fd == True:
                        for fd in fd_string:
                            left_fds.append(fd[0])
                            right_fds.append(fd[1])
                        break
                    else:
                        print(f"Invalid functional dependency was entered, please enter only valid functional dependencies")
    
        #loops until user submits a valid choice of form to normalize to
        form_choice = ""
        while True:
            form_choice = input("\nWhich form would you like to reach\n1: 1NF\n2: 2NF\n3: 3NF\nB: BCNF\n4: 4NF\n5: 5NF\n")
            if form_choice == '1' or '2' or '3' or 'B' or '4' or '5':
                break
            else:
                print("invalid choice selection")
    
        #if form to normalize to is 4NF or 5NF, user is warned that data tuples are required for the normalization process
        attributeindex = attributes
        data_instance_tuples = []
        if form_choice in ['4', '5']:
            print("\nFor 4NF normalization, you will need to add data instances for review.")
            print("Data instances will be connected to the initial attribute list, and therefore")
            print(f"must be the same length as the number of attributes that you input ({len(attributeindex)})")
            print("If multivalued data is present, should be entered in d1,d2 d3 form,")
            print("with a | instead of a comma meaning parts of a multivalued data tuple")
            print("For each data instance, separate each attribute's info by a comma ex: d1,d2,d3,d4 and type 'done' when finished")
            
            #loop accepts valid data tuples as input until user inputs 'done'
            while True:
                current_data_instance = input("Enter data instance or type 'done' to finish: ")
                if current_data_instance.lower() == 'done':
                    break
                data_tuple = []
                #inputs are split on commas for each attribute they are connected to, and "|" is used to separate parts of multivalued data
                for attribute in current_data_instance.split(","):
                    multivalued_data = attribute.split("|")
                    if len(multivalued_data) > 1:
                        data_tuple.append(tuple(multivalued_data))
                    else:
                        data_tuple.append(multivalued_data[0])
                if len(data_tuple) == len(attributeindex):
                    data_instance_tuples.append(tuple(data_tuple))
                else:
                    print("Invalid tuple")
            expanded_data_tuples = []

            #based on the multivalued attributes determined by user input, each selected attribute that includes "|" is split into separate tuples to remove non-atomic data
            for data_tuple in data_instance_tuples:
                attribute_values = []
                for i, value in enumerate(data_tuple):
                    if attributes[i] in multi_valued_attributes:
                        attribute_values.append(list(value) if isinstance(value, tuple) else [value])
                    else:
                        attribute_values.append([value])
                #creates updated tuple list based on multi-valued data
                for combination in product(*attribute_values):
                    expanded_data_tuples.append(combination)
            data_instance_tuples = expanded_data_tuples
            
        #if user selects 1NF-BCNF, user is notified that data tuples are optional, and will not be used for normalization
        else:
            print("\nIf you have data instances, you may enter them here. Since you are not normalizing to 4NF")
            print("or 5NF, these data instances are just for display purposes. Type 'done' if you don't want to add any")
            print("Data instances will be connected to the initial attribute list, and therefore")
            print(f"must be the same length as the number of attributes that you input ({len(attributeindex)})")
            print("If multivalued data is present, should be entered in d1,d2 d3 form,")
            print("with a | instead of a comma meaning parts of a multivalued data tuple")
            print("For each data instance, separate each attribute's info by a comma ex: d1,d2,d3,d4 and type 'done' when finished")
            
            #loop accepts valid data tuples as input until user inputs 'done'
            while True:
                current_data_instance = input("Enter data instance or type 'done' to finish: ")
                if current_data_instance.lower() == 'done':
                    break
                data_tuple = []
                #inputs are split on commas for each attribute they are connected to, and "|" is used to separate parts of multivalued data
                for attribute in current_data_instance.split(","):
                    multivalued_data = attribute.split("|")
                    if len(multivalued_data) > 1:
                        data_tuple.append(tuple(multivalued_data))
                    else:
                        data_tuple.append(multivalued_data[0])
                if len(data_tuple) == len(attributeindex):
                    data_instance_tuples.append(tuple(data_tuple))
                else:
                    print("Invalid tuple")
            expanded_data_tuples = []
            
            #based on the multivalued attributes determined by user input, each selected attribute that includes "|" is split into separate tuples to remove non-atomic data
            for data_tuple in data_instance_tuples:
                attribute_values = []
                for i, value in enumerate(data_tuple):
                    if attributes[i] in multi_valued_attributes:
                        attribute_values.append(list(value) if isinstance(value, tuple) else [value])
                    else:
                        attribute_values.append([value])

                #creates updated tuple list based on multi-valued data
                for combination in product(*attribute_values):
                    expanded_data_tuples.append(combination)
            data_instance_tuples = expanded_data_tuples

        #sets initial dictionary values to expected values from the user inputs
        tables[table_name]['attributes'] = attributes
        tables[table_name]['cand_keys'] = cand_keys
        tables[table_name]['multi_valued_attributes'] = multi_valued_attributes
        if functional_dependencies_exist == 'y':
            tables[table_name]['left_fds'] = left_fds
            tables[table_name]['right_fds'] = right_fds

        #normalization is called with the user's choice of what form to reach
        normalize_tables(tables, form_choice, data_instance_tuples, attributeindex)
    
        #output a formatted representation of the normalized relations
        for table, data in tables.items():
            print("\n" + "=" * 40)
            print(f"Table: {table}")
            print("-" * 40)
            #display attributes
            attributes = ', '.join(data['attributes'])
            print(f"Attributes: [{attributes}]")
            #retrieve and display relevant data
            relevant_data = get_connected_data(attributeindex, data_instance_tuples, data['attributes'])
            printed_pieces = set()  # Set to track unique data pieces
            print("Data Instances:")
            for data_piece in relevant_data:
                if data_piece not in printed_pieces:
                    print("  " + str(data_piece))
                    printed_pieces.add(data_piece)
            #display candidate keys
            if len(data['cand_keys']) == 0:
                data['cand_keys'] = data['attributes']
            candidate_keys = ', '.join([str(key) for key in data['cand_keys']])
            print(f"Candidate Keys: [{candidate_keys}]")
            print("=" * 40)


#function that normalizes a set of tables from 1NF-5NF depending on what the user selects
def normalize_tables(tables, form_choice, di_tuples, attributeindex):
    #create a temporary dictionary to hold new tables to avoid changing the original during iteration
    new_tables = {}
    
    #begin 1NF normalization
    for table, data in list(tables.items()):
        if form_choice in ['1', '2', '3', 'B', '4', '5']:
            multi_valued_attributes = data['multi_valued_attributes']
            if multi_valued_attributes:
                
                #create separate tables for each multi-valued attribute
                for mv_attr in multi_valued_attributes:
                    new_table_name = f"{table}_{mv_attr}_1NF"
                    new_table_attributes = [mv_attr] + [key for sublist in data['cand_keys'] for key in sublist if key != mv_attr]
                    
                    #add the new table to the temporary dictionary
                    new_tables[new_table_name] = {
                        'attributes': new_table_attributes,
                        'cand_keys': data['cand_keys'],
                        'multi_valued_attributes': [],
                        'left_fds': [],
                        'right_fds': []
                    }
                    
                #remove multi-valued attributes from the original table
                tables[table]['attributes'] = [attr for attr in data['attributes'] if attr not in multi_valued_attributes]
                tables[table]['multi_valued_attributes'] = []
                
                #move related functional dependencies
                for left, right in zip(data['left_fds'], data['right_fds']):
                    for mv_attr in multi_valued_attributes:
                        if mv_attr in left or mv_attr in right:
                            new_fd_table_name = f"{table}_{mv_attr}_1NF"
                            new_tables[new_fd_table_name]['left_fds'].append(left)
                            new_tables[new_fd_table_name]['right_fds'].append(right)
                            new_tables[new_fd_table_name]['attributes'] = []
                            new_tables[new_fd_table_name]['cand_keys'] = []
                            new_tables[new_fd_table_name]['cand_keys'].append(left)
                            
                            #add any missing attributes to the new table
                            for attr in left + right:
                                if attr not in new_tables[new_fd_table_name]['attributes']:
                                    new_tables[new_fd_table_name]['attributes'].append(attr)

                #remove functional dependencies that are no longer relevant to the original table
                new_functional_dependencies = [
                    (left, right) for left, right in zip(data['left_fds'], data['right_fds'])
                    if not any(attr in left for attr in multi_valued_attributes) and not any(attr in right for attr in multi_valued_attributes)
                ]
                tables[table]['left_fds'], tables[table]['right_fds'] = zip(*new_functional_dependencies) if new_functional_dependencies else ([], [])
                
                #filter candidate keys for original table if they were affected by normalization
                new_cand_keys = []
                for cand_key in data['cand_keys']:
                    if all(attr in tables[table]['attributes'] for attr in cand_key):
                        new_cand_keys.append(cand_key)
                data['cand_keys'] = new_cand_keys
                if len(data['cand_keys']) == 0:
                    data['cand_keys'] = data['attributes']
   
    #replace previous tables with updated 1NF normalized tables if needed
    tables.update(new_tables)

    #begin 2NF normalization if selected by user
    for table, data in list(tables.items()):
        if form_choice in ['2', '3', 'B', '4', '5']:
            cand_keys = data['cand_keys']
            if len(cand_keys) > 0:
                for composite_key in cand_keys:
                    if len(composite_key) > 1:
                        new_fds_left = []
                        new_fds_right = []
                        transferred_fds_indices = set()

                        for i in range(len(data['left_fds'])):
                            left = data['left_fds'][i]
                            right = data['right_fds'][i]

                            #check for if functional dependency is a partial dependency
                            if set(left).issubset(set(composite_key)) and set(left) != set(composite_key):
                                #create a new table for the partial dependency
                                new_table_name = f"{table}_{'_'.join(left)}_2NF"
                                new_table_attributes = list(set(left + right))
                                new_tables[new_table_name] = {
                                    'attributes': new_table_attributes,
                                    'cand_keys': [left],
                                    'multi_valued_attributes': [],
                                    'left_fds': [],
                                    'right_fds': []
                                }

                                #move dependencies involving attributes in 'right' to the new table
                                for j in range(len(data['left_fds'])):
                                    l_fd = data['left_fds'][j]
                                    r_fd = data['right_fds'][j]
                                    if any(attr in right for attr in l_fd + r_fd):
                                        new_tables[new_table_name]['left_fds'].append(l_fd)
                                        new_tables[new_table_name]['right_fds'].append(r_fd)
                                        transferred_fds_indices.add(j)

                                #remove attributes involved in the partial dependency from the original table
                                tables[table]['attributes'] = [attr for attr in data['attributes'] if attr not in right]
                            else:
                                new_fds_left.append(left)
                                new_fds_right.append(right)

                        #remove functional dependencies that were moved to the new table
                        tables[table]['left_fds'] = [fd for idx, fd in enumerate(new_fds_left) if idx not in transferred_fds_indices]
                        tables[table]['right_fds'] = [fd for idx, fd in enumerate(new_fds_right) if idx not in transferred_fds_indices]

    #replace previous tables with updated 2NF normalized tables if needed
    tables.update(new_tables)
   
    #begin 3NF normalization if selected by user
    for table, data in list(tables.items()):
        if form_choice in ['3', 'B', '4', '5']:
            prime_attributes = set(attr for key in cand_keys for attr in key)
            #check each functional dependency X->Y to see if X is not a superkey or Y is not a prime attribute
            for left, right in zip(data['left_fds'], data['right_fds']):
                if not any(set(left).issuperset(set(key)) for key in data['cand_keys']) and not set(right).issubset(prime_attributes):
                    #create a new table for this violation
                    new_table_name = f"{table}_{'_'.join(left)}_3NF"
                    new_table_attributes = list(set(left + right))
                    new_tables[new_table_name] = {
                        'attributes': new_table_attributes,
                        'cand_keys': [left],
                        'multi_valued_attributes': [],
                        'left_fds': [left],
                        'right_fds': [right]
                    }
                    data['left_fds'] = list(data['left_fds'])
                    data['right_fds'] = list(data['right_fds'])
                    #remove the dependency from the original table
                    data['left_fds'].remove(left)
                    data['right_fds'].remove(right)
                    #remove the non-prime attributes from the original table
                    tables[table]['attributes'] = [attr for attr in data['attributes'] if attr not in right]

        #if there are still FDs left, keep them in the original table
        if data['left_fds'] and data['right_fds']:
            tables[table]['left_fds'] = data['left_fds']
            tables[table]['right_fds'] = data['right_fds']
        else:
            tables[table]['left_fds'] = []
            tables[table]['right_fds'] = []
   
    #replace previous tables with updated 3NF normalized tables if needed
    tables.update(new_tables)    
   
    #begin BCNF normalization until all BCNF violations have been resolved if selected by user
    bcnf_completed = False
    while bcnf_completed == False:  
        bcnf_completed = True 
        for table, data in list(tables.items()):
            if form_choice in ['B', '4', '5']:
                #check each functional dependency X->Y to see if X is not a superkey
                for left, right in zip(data['left_fds'], data['right_fds']):
                    is_superkey = False
                    for key in data['cand_keys']:
                        if left == key:
                            is_superkey = True
                    if is_superkey == False:
                        bcnf_completed = False
                        data['attributes'] = [attr for attr in data['attributes'] if attr not in right]
                        #create a new table for this violation
                        new_table_name = f"{table}_{'_'.join(left)}_BCNF"
                        new_table_attributes = list(set(left + right))
                        new_tables[new_table_name] = {
                            'attributes': new_table_attributes,
                            'cand_keys': [left],
                            'multi_valued_attributes': [],
                            'left_fds': [left],
                            'right_fds': [right]
                        }
                        data['left_fds'] = list(data['left_fds'])
                        data['right_fds'] = list(data['right_fds'])
                        #remove the dependency from the original table
                        data['left_fds'].remove(left)
                        data['right_fds'].remove(right)
                        #remove the non-prime attributes from the original table
                        data['cand_keys'] = [key for key in data['cand_keys'] if not set(right).intersection(set(key))]

            #if there are still FDs left, keep them in the original table
            if data['left_fds'] and data['right_fds']:
                tables[table]['left_fds'] = data['left_fds']
                tables[table]['right_fds'] = data['right_fds']
            else:
                tables[table]['left_fds'] = []
                tables[table]['right_fds'] = []
                
    #replace previous tables with updated BCNF normalized tables if needed
    tables.update(new_tables)        

    #begin 4NF normalization if selected by user
    for table, data in list(tables.items()):
        if form_choice in ['4', '5']:
            
            mvfound = False
            input_atts = data['attributes']
            input_atts_length = len(input_atts)
            selected_data = get_connected_data(attributeindex, di_tuples, input_atts)

            #check for first portion of MVD
            col1 = 0
            while col1 < input_atts_length:
                first_stage_dupes = count_column_duplicates(selected_data, col1, 4)
                for dupe in first_stage_dupes:
                    grouped_tuples = gather_tuples_by_duplicate(selected_data, col1, dupe)
                    
                    #check for second portion of MVD
                    col2 = 0
                    while col2 < input_atts_length:
                        if col2 != col1:
                            second_stage_dupes = count_column_duplicates(grouped_tuples, col2, 2)
                            gathered_full_list = []
                            for dupe1 in second_stage_dupes:
                                for dupe2 in second_stage_dupes:
                                    if dupe1 != dupe2:
                                        grouped_tuplesd1 = gather_tuples_by_duplicate(grouped_tuples, col2, dupe1)
                                        grouped_tuplesd2 = gather_tuples_by_duplicate(grouped_tuples, col2, dupe2)
                                        grouped_tuples_list = [grouped_tuplesd1, grouped_tuplesd2]
                                        gathered_full_list.append(grouped_tuples_list)
                            for grouped_tuples_list in gathered_full_list:
                                
                                #check for third portion of MVD
                                col3 = 0
                                while col3 < input_atts_length:
                                    if (col3 != col1) and (col3 != col2):
                                        k=0
                                        while k < len(grouped_tuples_list):
                                            third_stage_dupes = count_column_duplicates(grouped_tuples_list[k], col3, 1)
                                            i=0
                                            while i < len(grouped_tuples_list):
                                                if i != k:
                                                    matches_found = 0
                                                    usedattr = ''
                                                    for attr in third_stage_dupes:
                                                        j=0
                                                        while j < len(grouped_tuples_list[i]):
                                                            if (attr == grouped_tuples_list[i][j][col3]) and (usedattr != attr):
                                                                usedattr = attr
                                                                matches_found += 1
                                                            j+=1
                                                    #begin normalization process if MVD successfully detected
                                                    if (matches_found == 2) and (mvfound == False):
                                                        mvfound = True
                                                        
                                                        #create new tables to separate the two MVD attributes
                                                        table_name = f"{table}_MVD_decomposition"
                                                        #adds details to first table
                                                        table1_name = f"{table_name}_{attributeindex[col2]}_4NF"
                                                        table1_attributes = [attr for attr in data['attributes'] if attr != attributeindex[col2]]
                                                        new_tables[table1_name] = {
                                                            'attributes': table1_attributes,
                                                            'cand_keys': data['cand_keys'],
                                                            'multi_valued_attributes': data['multi_valued_attributes'],
                                                            'left_fds': data['left_fds'],
                                                            'right_fds': data['right_fds']
                                                        }
                                                        #adds details to second table
                                                        table2_name = f"{table_name}_{attributeindex[col3]}_4NF"
                                                        table2_attributes = [attr for attr in data['attributes'] if attr != attributeindex[col3]]
                                                        new_tables[table2_name] = {
                                                            'attributes': table2_attributes,
                                                            'cand_keys': data['cand_keys'],
                                                            'multi_valued_attributes': data['multi_valued_attributes'],
                                                            'left_fds': data['left_fds'],
                                                            'right_fds': data['right_fds']
                                                        }                                                     
                                                        left_fd_to_add = []
                                                        right_fd_to_add = []
                                                        #filter related functional dependencies for first table
                                                        for left, right in zip(data['left_fds'], data['right_fds']):
                                                            if all(attr in table1_attributes for attr in left) and all(attr in table1_attributes for attr in right):
                                                                left_fd_to_add.append(left)
                                                                right_fd_to_add.append(right)
                                                        left_fd_to_add2 = []
                                                        right_fd_to_add2 = []
                                                        #filter related functional dependencies for second table
                                                        for left, right in zip(data['left_fds'], data['right_fds']):
                                                            if all(attr in table2_attributes for attr in left) and all(attr in table2_attributes for attr in right):
                                                                left_fd_to_add2.append(left)
                                                                right_fd_to_add2.append(right)
                                                        data['left_fds'] = []
                                                        data['right_fds'] = []
                                                        #add valid FDs to the new tables
                                                        new_tables[table1_name]['left_fds'] = left_fd_to_add
                                                        new_tables[table1_name]['right_fds'] = right_fd_to_add  
                                                        new_tables[table2_name]['left_fds'] = left_fd_to_add2
                                                        new_tables[table2_name]['right_fds'] = right_fd_to_add2
                                                        
                                                        #remove the original table now that the two replacements have been created
                                                        del tables[table]
                                                i+=1
                                            k+=1
                                    col3+=1
                        col2+=1
                col1+=1
                    
    #replace previous tables with updated 4NF normalized tables if needed
    tables.update(new_tables)
    
    #begin 5NF normalization process if selected by user
    jd_found = False
    for table, data in list(tables.items()):
        if form_choice == '5':
            #create all possible combinations of attributes that could create a join dependency
            possible_join_groups = generate_attribute_groups(data['attributes'])
            for attrset in possible_join_groups:
                input_atts = attrset[0]
                input_atts_length = len(input_atts)
                selected_data = get_connected_data(data['attributes'], di_tuples, input_atts)
                input_atts2 = attrset[1]
                selected_data2 = get_connected_data(data['attributes'], di_tuples, input_atts2)
                j=0
                for attr in attrset[0]:
                    if attr == attrset[2]:
                        col1 = j
                    j+=1   
                j=0
                for attr in attrset[1]:
                    if attr == attrset[2]:
                        col2 = j
                    j+=1
                joined_tuples = []
                
                #create a dictionary from the second list for quick lookup
                tuples_dict = {tup[col2]: tup for tup in selected_data2}
                
                for tup1 in selected_data:
                    key = tup1[col1]
                    if key in tuples_dict:
                        tup2 = tuples_dict[key]
                        #join the tuples but exclude the join column from the second tuple
                        joined_tuple = tup1 + tup2[:col2] + tup2[col2 + 1:]
                        joined_tuples.append(joined_tuple)
                i=0
                set1 = {frozenset(tup) for tup in di_tuples}
                set2 = {frozenset(tup) for tup in joined_tuples}
                #return True if the two sets are identical, otherwise False
                if set1 == set2:
                    tuples_matching = True
                else:
                    tuples_matching = False
                
                #if tuples are found to be matching and a join dependency has not already been found, begin normalizing table to 5NF
                if (tuples_matching == True) and (jd_found == False):
                    jd_found = True
                    table_name = f"{table}"
                    #create table1 based on attributes from attrset[0]
                    table1_name = f"{table_name}_join1_5NF"
                    table1_attributes = attrset[0]
                    new_tables[table1_name] = {
                        'attributes': table1_attributes,
                        'cand_keys': [],
                        'multi_valued_attributes': data['multi_valued_attributes'],
                        'left_fds': data['left_fds'],
                        'right_fds': data['right_fds']
                    }
                    #create table2 based on attributes from attrset[1]
                    table2_name = f"{table_name}_join2_5NF"
                    table2_attributes = attrset[1]
                    new_tables[table2_name] = {
                        'attributes': table2_attributes,
                        'cand_keys': [],
                        'multi_valued_attributes': data['multi_valued_attributes'],
                        'left_fds': data['left_fds'],
                        'right_fds': data['right_fds']
                    }
                    #filter related functional dependencies for first table
                    left_fd_to_add1 = []
                    right_fd_to_add1 = []
                    for left, right in zip(data['left_fds'], data['right_fds']):
                        if all(attr in table1_attributes for attr in left) and all(attr in table1_attributes for attr in right):
                            left_fd_to_add1.append(left)
                            right_fd_to_add1.append(right)
                    #filter related functional dependencies for second table
                    left_fd_to_add2 = []
                    right_fd_to_add2 = []
                    for left, right in zip(data['left_fds'], data['right_fds']):
                        if all(attr in table2_attributes for attr in left) and all(attr in table2_attributes for attr in right):
                            left_fd_to_add2.append(left)
                            right_fd_to_add2.append(right)
                    #filter candidate keys for first table
                    for cand_key in data['cand_keys']:
                        if all(attr in table1_attributes for attr in cand_key):
                            new_tables[table1_name]['cand_keys'].append(cand_key)
                    #filter candidate keys for second table
                    for cand_key in data['cand_keys']:
                        if all(attr in table2_attributes for attr in cand_key):
                            new_tables[table2_name]['cand_keys'].append(cand_key)
                    #update tables with valid FDs
                    new_tables[table1_name]['left_fds'] = left_fd_to_add1
                    new_tables[table1_name]['right_fds'] = right_fd_to_add1
                    new_tables[table2_name]['left_fds'] = left_fd_to_add2
                    new_tables[table2_name]['right_fds'] = right_fd_to_add2

                    #remove the original table since it can be replaced by the two new tables
                    del tables[table]
    
    #replace previous tables with updated 5NF fully normalized tables if needed
    tables.update(new_tables)

#4NF connected function for counting how many of each value appear in an attribute's column
def count_column_duplicates(tuples_list, col_index, dupe_amount):
    column_data = [row[col_index] for row in tuples_list]
    counts = Counter(column_data)
    duplicates = {attr: count for attr, count in counts.items() if count >= dupe_amount}
    return duplicates

#4NF connected function that collects tuples that contain a duplicate value in a specific column
def gather_tuples_by_duplicate(tuples_list, col_index, duplicate):
    gathered_tuples = []
    matching_tuples = [tup for tup in tuples_list if tup[col_index] == duplicate]
    gathered_tuples.extend(matching_tuples)
    return gathered_tuples

#function that collects unique tuples related to selected attributes with duplicates removed
def get_connected_data(attributes, data_instance_tuples, selected_attributes):
    connected_data = []
    seen_tuples = set()
    attribute_index_map = {attr: idx for idx, attr in enumerate(attributes)}
    for instance in data_instance_tuples:
        instance_data = tuple(instance[attribute_index_map[attr]] for attr in selected_attributes if attr in attribute_index_map)
        if instance_data not in seen_tuples:
            seen_tuples.add(instance_data)
            connected_data.append(instance_data)
    return connected_data

def generate_attribute_groups(attributes):
    #convert the list of attributes into a set for easier operations
    attr_set = set(attributes)
    result = []
    #iterate over each attribute, treating it as the "joiningattr"
    for joiningattr in attributes:
        remaining_attrs = attr_set - {joiningattr}
        for r1 in range(1, len(remaining_attrs)):
            for group1 in combinations(remaining_attrs, r1):
                group1_set = set(group1) | {joiningattr}
                group2_set = remaining_attrs - group1_set | {joiningattr}
                #both group1 and group2 must have at least 2 attributes (including joiningattr)
                if len(group1_set) >= 2 and len(group2_set) >= 2:
                    result.append((tuple(group1_set), tuple(group2_set), joiningattr))
    return result

input_parser()