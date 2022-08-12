import argparse
import matplotlib.pyplot as plt 
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(description="A program to sort the contents of 2 Sequence Read Files based on the index barcodes \n Fastq files must be zipped.")
    parser.add_argument("-f", "--data_file", help="Passes file containing data from demux script.", type=str,required=True)
    return parser.parse_args()


args = get_args()
data_file = args.data_file


file_dict = {}
hopped_dict = {}

#Open data file with file names and record count.  Also has index pairs and amount of hopping
with open(data_file,'r') as fh:
    record_count = 0
    for line in fh:
        line = line.strip()
        #Reads in filenames and number of records
        if 'fastq' in line:
            record = line.split('\t\t')
            file_dict[record[0][3:-6]] = int(record[1])
            if 'r2' in line:
                record_count += int(record[1]) #Counts number of total records
        #Reads in hopped index pairs and number of hops
        elif '-' in line:
            record = line.split('\t\t')
            hopped_dict[record[0]] = int(record[1])


#Creates dictionary where key is the tuple with 2 elements- each index that is hopped.
hopped_indexes = {}
for keys,values in hopped_dict.items():
    hopped_indexes[tuple(keys.split('-'))] = values

#Creates column and row vectors for use in plot.
columns = list(set([i[0] for i in hopped_indexes.keys()]))
columns.sort()
rows = columns.copy()

#Populate 2d array, (24x24 matrix) with the index pairs and corresponding number of occurences
hopped_array = np.zeros((len(columns),len(rows)))

for col_num,col_val in enumerate(columns):
    for row_num,row_val in enumerate(rows):
        if col_val == row_val:
            hopped_array[col_num,row_num] = np.log10(file_dict[col_val])
        else:
            hopped_array[col_num,row_num] = np.log10(hopped_indexes[(col_val,row_val)])




#Creates the heatmap
plt.figure(1)
fig, ax = plt.subplots(figsize = (50,32))
im = ax.imshow(hopped_array,cmap = 'seismic')

# # Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(columns)), labels=columns,rotation = 90,fontsize = 20)
ax.set_yticks(np.arange(len(rows)), labels=rows, fontsize = 20)

# # Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=90, ha="center")

# #Loop over data dimensions and create text annotations.
for i in range(len(columns)):
     for j in range(len(rows)):
         text = ax.text(j, i,np.round(hopped_array[i, j],2), ha="center", va="center", color="w", fontsize = 15)

ax.set_title("Log10 Number of Index Pair Occurences", fontsize = 40)
fig.tight_layout()
plt.savefig('test_heatmap.png')




filename = file_dict.keys()
percent_occurence = [np.round(items/record_count*100,2) for items in file_dict.values()]
fig.clear(True)


plt.figure(2)
plt.figure(figsize = (30,20))
plt.bar(filename,percent_occurence)
plt.title('Number of Records by Type', fontsize = 30)
plt.xlabel('Index Type',fontsize = 20)
plt.ylabel('Percent of Occurences', fontsize = 20)

plt.savefig('num_occurences.png')