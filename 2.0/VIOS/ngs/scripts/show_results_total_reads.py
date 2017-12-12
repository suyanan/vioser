#-*- coding:utf-8 -*-

#from .config_paras import *

import os
import django

from .config_paras import *
from .show_results_blastn import *
from matplotlib.pyplot import *
from collections import Counter


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'VIOS.settings'
    django.setup()


def files_reads_conter(querySample):
	"""for fig1-3 data sources"""
	#raw fastq file
	reads_raw_datas_file = os.path.join(trimmomatic_path,querySample+'_trimlog.txt')
	
	#after AC, four fastq file
	reads_after_qc_P_file = os.path.join(trimmomatic_path,querySample+'_output_forward_paired.fastq')
	reads_after_qc_FU_file = os.path.join(trimmomatic_path,querySample+'_output_forward_unpaired.fastq')
	reads_after_qc_RU_file = os.path.join(trimmomatic_path,querySample+'_output_reverse_unpaired.fastq')
	reads_after_qc_se_output_file = os.path.join(trimmomatic_path,querySample+'_output.fastq')

	#after map GH_HG fastq file
	reads_after_map_hg38_P_file = os.path.join(bowtie2_path,querySample+'_pair_host.1.fastq')
	reads_after_map_hg38_U_file = os.path.join(bowtie2_path,querySample+map_gb_hg_singleAndunpair_fastq_file_suffix)

	#after map NT_VIRUSE fastq file
	reads_after_map_viruses_P_file = os.path.join(bowtie2_path,querySample+'_pair_VIRUS.1.fastq')
	reads_after_map_viruses_U_file = os.path.join(bowtie2_path,querySample+map_nt_viruses_singleAndunpair_fastq_file_suffix)
	reads_after_map_viruses_SAM_file = os.path.join(bowtie2_path,querySample+map_nt_viruses_singleAndunpair_sam_file_suffix)
	
	reads_counter_file = os.path.join(result_total_sta_path,'pipeline_reads_sta.txt')
	if os.path.exists(reads_after_qc_P_file):
		os.system('wc -l %s %s %s %s %s %s %s %s %s > %s'
			%(reads_raw_datas_file,
				reads_after_qc_P_file,reads_after_qc_FU_file,reads_after_qc_RU_file,
				reads_after_map_hg38_P_file,reads_after_map_hg38_U_file,
				reads_after_map_viruses_P_file,reads_after_map_viruses_U_file,reads_after_map_viruses_SAM_file,
				reads_counter_file))
		with open(reads_counter_file,'r')  as reads_counter_file_obj:
			reads_counter_lines_list = reads_counter_file_obj.readlines()
			reads_raw_datas_numbers = int(reads_counter_lines_list[0].split(' ')[0:-1][-1])
			reads_after_qc_numbers = (int(reads_counter_lines_list[1].split(' ')[0:-1][-1])*2+int(reads_counter_lines_list[2].split(' ')[0:-1][-1])+int(reads_counter_lines_list[3].split(' ')[0:-1][-1]))/4
			reads_after_map_hg38_numbers = (int(reads_counter_lines_list[4].split(' ')[0:-1][-1])*2+int(reads_counter_lines_list[5].split(' ')[0:-1][-1]))/4
			reads_after_map_viruses_numbers = (int(reads_counter_lines_list[6].split(' ')[0:-1][-1])*2+int(reads_counter_lines_list[7].split(' ')[0:-1][-1]))/4
			reads_after_map_viruses_SAM_numbers = int(reads_counter_lines_list[8].split(' ')[0:-1][-1])##not equal to reads_after_map_viruses_numbers
			return reads_raw_datas_numbers, reads_after_qc_numbers, reads_after_map_hg38_numbers, reads_after_map_viruses_numbers,reads_after_map_viruses_SAM_numbers
	else:
		print '===================dfasfasfsfa=================='
		os.system('wc -l %s %s %s %s %s > %s'
			%(reads_raw_datas_file,
				reads_after_qc_se_output_file,
				reads_after_map_hg38_U_file,
				reads_after_map_viruses_U_file,reads_after_map_viruses_SAM_file,
				reads_counter_file))
		with open(reads_counter_file,'r') as reads_counter_file_obj:
			reads_counter_lines_list = reads_counter_file_obj.readlines()
			reads_raw_datas_numbers = int(reads_counter_lines_list[0].split(' ')[0:-1][-1])
			reads_after_qc_numbers = int(reads_counter_lines_list[1].split(' ')[0:-1][-1])/4
			reads_after_map_hg38_numbers = int(reads_counter_lines_list[2].split(' ')[0:-1][-1])/4
			reads_after_map_viruses_numbers = int(reads_counter_lines_list[3].split(' ')[0:-1][-1])/4
			reads_after_map_viruses_SAM_numbers = int(reads_counter_lines_list[4].split(' ')[0:-1][-1])##not equal to reads_after_map_viruses_numbers
			return reads_raw_datas_numbers, reads_after_qc_numbers, reads_after_map_hg38_numbers, reads_after_map_viruses_numbers,reads_after_map_viruses_SAM_numbers

		
def reads_fig4_data_sources(querySample):
	"""for fig4 data sources"""
	reads_after_map_viruses_file = os.path.join(bowtie2_path,querySample+map_nt_viruses_singleAndunpair_sam_file_suffix)
	#print reads_after_map_viruses_file
	with open(reads_after_map_viruses_file,'r') as reads_after_map_viruses_file_obj:
		reads_lines = reads_after_map_viruses_file_obj.readlines()
		reads_fig4_data_list = []
		for i in range(len(reads_lines)):
			each_accesion = reads_lines[i].split('\t')[2]
			reads_fig4_data_list.append(each_accesion)
		return reads_fig4_data_list


def pipeline_reads_sta_to_grafic(querySample,ntVirusesFamilyName):

	reads_raw_datas_numbers, reads_after_qc_numbers, reads_after_map_hg38_numbers, reads_after_map_viruses_numbers, reads_after_map_viruses_SAM_numbers = files_reads_conter(querySample)
	
	fig = figure(figsize=(15,5),dpi=80)
	
	#fig = figure()

	##fenzi(numerator) and fenmu(denominator)
	#fig1: qc process, before and after,reads_raw_datas_numbers, reads_after_qc_numbers
	p1 = subplot(2,3,1)
	reads_qc_list = [reads_after_qc_numbers,reads_raw_datas_numbers-reads_after_qc_numbers]
	#print reads_qc_list
	labels_reads_qc_list = ['after QC','filtered']
	explode = [0.05,0]
	p1.pie(reads_qc_list,explode=explode,shadow=True,labels=labels_reads_qc_list,startangle=90,labeldistance=1.1,pctdistance=0.6)
	p1.axis('equal')
	
	#fig2: map_hg38 process, before and after,reads_after_qc_numbers, reads_after_map_hg38_numbers
	p2 = subplot(2,3,2)
	reads_map_hg38_list = [reads_after_map_hg38_numbers,reads_after_qc_numbers-reads_after_map_hg38_numbers]
	#print reads_map_hg38_list
	label_reads_map_hg38_list = ['non-host','filtered host']
	p2.pie(reads_map_hg38_list,explode=explode,shadow=True,labels=label_reads_map_hg38_list,startangle=0,labeldistance=1.1,pctdistance=0.6)
	p2.axis('equal')

	#fig3: map_viruses process ,before and after,reads_after_map_hg38_numbers,reads_after_map_viruses_numbers
	p3 = subplot(2,3,3)
	reads_map_viruses_list = [reads_after_map_viruses_numbers,reads_after_map_hg38_numbers-reads_after_map_viruses_numbers]
	#print reads_map_viruses_list
	label_reads_map_viruses_list = ['viruses','others']
	p3.pie(reads_map_viruses_list,explode=explode,shadow=True,labels=label_reads_map_viruses_list,startangle=0,labeldistance=1.1,pctdistance=0.6)
	p3.axis('equal')


	##fig4: reads statistics about top 10 virus in SAM file.
	reads_fig4_data = reads_fig4_data_sources(querySample)
	#print reads_fig4_data  #[..., 'AB256208.1', 'AB256497.1', 'AB256497.1', '*']
	#print len(reads_fig4_data)	

	counter = Counter(reads_fig4_data)
	#print counter  ##Counter({'KF429752.1': 13, ..., 'FJ943620.1': 1})	#<class 'collections.Counter'>
	counter_most = counter.most_common(setShowTopLines-5)  ##!!!get most common(improper!!!), not map aginst bacteria, results may include bacteria.
	#print counter_most  ##[('KF429752.1', 13), ('KF268195.1', 12), ('KF429748.1', 9), ('JN860680.1', 8), ('KF268315.1', 8), ('AY601636.1', 8), ('JX423386.1', 8), ('HC084950.1', 7), ('KF268120.1', 7), ('FJ025928.1', 7)]	<type 'list'>
	counter_most_dict = dict(counter_most)
	#print counter_most_dict  ##{'KF268120.1': 7, 'KF429748.1': 9, 'KF429752.1': 13, 'FJ025928.1': 7, 'KF268315.1': 8, 'JN860680.1': 8, 'HC084950.1': 7, 'KF268195.1': 12, 'AY601636.1': 8, 'JX423386.1': 8}
	
	counter_most_dict_sorted_list = sorted(counter_most_dict.items(),key=lambda item:item[1],reverse = True) #[('KM209255.1', 5868), ('KM209277.1', 1973), 

	accession_data = []
	counter_data = []
	for i in range(len(counter_most_dict_sorted_list)):
		accession_data.append(counter_most_dict_sorted_list[i][0])
		counter_data.append(counter_most_dict_sorted_list[i][1])
		#print accession_data  #just counter the 3rd colomn, not 7th colomn(mayby include the accession string)

	##change accesion to annotation
	annotation_data = []
	for i in range(len(accession_data)):
		annotation = search_nt_title(ntVirusesFamilyName,accession_data[i])
		annotation_data.append(annotation)

	annotation_data.append('other viruses')
	counter_data.append(reads_after_map_viruses_SAM_numbers-sum(counter_data))	
	#print annotation_data  #['CP002121.1', 'KP279748.1', 'CP016318.1', 'KX494979.1', 'AM420293.1', 'FN997652.1', 'CP008698.1', 'CP000233.1', 'AB256208.1', 'KY065497.1', 'others viruses']
	#print counter_data  #[10335, 3922, 195, 3715, 432, 291, 264, 346, 317, 1619, 1599]

	#p4 = subplot(2,1,2)  #the before 3 figs was (2,1,1)
	p4 = subplot(2,3,4)  #the before 3 figs was (2,1,1)
	#p4.pie(counter_data,shadow=True,labels=annotation_data,autopct='%2.1f%%',startangle=0,labeldistance=1.1,pctdistance=0.6)
	p4.pie(counter_data,shadow=True,autopct='%2.1f%%',startangle=0,labeldistance=1.1,pctdistance=0.6)
	p4.axis('equal')
	subplots_adjust(left=-0.1,right=1.1,wspace=-0.6)
	#legend(annotation_data)
	legend(annotation_data,loc='top right',bbox_to_anchor=(0.58,0.86))	
	#subplots_adjust(bottom=0.2)
	#tight_layout(h_pad=2)
	title_str = "%s reads changes while processing"%(querySample)
	#title("%s reads changes while processing"%(querySample))
	text(1.6,-1.4,title_str,fontsize=14)

	fig_file = os.path.join(result_total_sta_path,'sta_reads_'+querySample+'.png')
	fig.savefig(fig_file)
	show()


def pipeline_identifer_list(querySample,ntVirusesFamilyName):
	##statistics:reads_after_map_viruses_SAM_numbers
	reads_raw_datas_numbers, reads_after_qc_numbers, reads_after_map_hg38_numbers, reads_after_map_viruses_numbers, reads_after_map_viruses_SAM_numbers = files_reads_conter(querySample)
	
	##fig4: reads statistics about top 10 virus in SAM file.
	reads_fig4_data = reads_fig4_data_sources(querySample)
	#print reads_fig4_data  #[..., 'AB256208.1', 'AB256497.1', 'AB256497.1', '*']

	counter = Counter(reads_fig4_data)
	#print counter  ##Counter({'KF429752.1': 13, ..., 'FJ943620.1': 1})	#<class 'collections.Counter'>
	
	counter_most = counter.most_common(setShowTopLines+20)  ##!!!get most common(improper!!!), not map aginst bacteria, results may include bacteria.
	#print counter_most  ##[('KF429752.1', 13), ('KF268195.1', 12), ('KF429748.1', 9), ('JN860680.1', 8), ('KF268315.1', 8), ('AY601636.1', 8), ('JX423386.1', 8), ('HC084950.1', 7), ('KF268120.1', 7), ('FJ025928.1', 7)]	<type 'list'>
	counter_most_dict = dict(counter_most)
	#print counter_most_dict  ##{'KF268120.1': 7, 'KF429748.1': 9, 'KF429752.1': 13, 'FJ025928.1': 7, 'KF268315.1': 8, 'JN860680.1': 8, 'HC084950.1': 7, 'KF268195.1': 12, 'AY601636.1': 8, 'JX423386.1': 8}
	
	counter_most_dict_sorted_list = sorted(counter_most_dict.items(),key=lambda item:item[1],reverse = True) #[('KM209255.1', 5868), ('KM209277.1', 1973), 

	##TABLE: 4 COLOMN (accession annotation number ratio)
	accession_data = []
	counter_data = []
	for i in range(len(counter_most_dict_sorted_list)):
		accession_data.append(counter_most_dict_sorted_list[i][0])
		counter_data.append(counter_most_dict_sorted_list[i][1])
		#print accession_data  #just counter the 3rd colomn, not 7th colomn(mayby include the accession string)
	
	##change accesion to annotation
	annotation_data = []
	for i in range(len(accession_data)):
		annotation = search_nt_title(ntVirusesFamilyName,accession_data[i])
		annotation_data.append(annotation)

	accession_data.append('the left')
	annotation_data.append('left viruses')
	counter_data.append(reads_after_map_viruses_SAM_numbers-sum(counter_data))	
	#print annotation_data  #['CP002121.1', 'KP279748.1', 'CP016318.1', 'KX494979.1', 'AM420293.1', 'FN997652.1', 'CP008698.1', 'CP000233.1', 'AB256208.1', 'KY065497.1', 'others viruses']
	#print counter_data  #[10335, 3922, 195, 3715, 432, 291, 264, 346, 317, 1619, 1599]

	counterRatio_data = []
	for i in range(len(counter_data)):
		eachRatio = format(float(counter_data[i])/float(reads_after_map_viruses_SAM_numbers),'.4f')
		counterRatio_data.append(eachRatio)

	identifer_data2D = []
	for i in range(len(counter_data)):
		each_line = [accession_data[i],annotation_data[i],counter_data[i],counterRatio_data[i]]
		identifer_data2D.append(each_line)
	return identifer_data2D



####CONTIGS
def nt_filter_target_accessionLength(fromBigFile,queryTheAccession):
    '''
    too slow ,need to modify
    '''
    with open(fromBigFile, 'r') as fromBigFile_obj:
        lines_list = fromBigFile_obj.readlines()
        lines_list_len = len(lines_list)
        keys_accession_list = []
        keys_accession_index_list = []
        for i in range(len(lines_list)):
            if lines_list[i][0] == '>':
                keys_accession_list.append(lines_list[i].strip('\n'))
                keys_accession_index_list.append(i)
        keys_accession_index_list.append(lines_list_len)

        values_seq_list = []
        for i in range(1, len(keys_accession_index_list)):
            values_seq_one_list = []
            for j in range(keys_accession_index_list[i - 1] + 1, keys_accession_index_list[i]):
                values_seq_one = lines_list[j].strip('\n')
                values_seq_one_list.append(values_seq_one)                
            values_seq_list.append(values_seq_one_list)  # before values_seq_one_list = [], append
 

        for i in range(len(keys_accession_list)):
        	accession = keys_accession_list[i].split(' ')[0].split('>')[-1]
        	if accession == queryTheAccession:
        		accession_length_sum = []
        		for j in range(len(values_seq_list[i])):
        			one_line_length = len(values_seq_list[i][j])
        			accession_length_sum.append(one_line_length)
        		return sum(accession_length_sum)

def pipeline_contigs_sta_to_grafic(ntVirusesFamilyName,querySample,blastnColumn,queryTheAccession):
	'''
	just show one target accession's contigs in blastn output.
	##paras:
	#blastPathSorted:blast_path_sorted=result_path+'blast_result_sorted_by_%s/'%(colNumSortedStr)
	#querySample: query_sample = 'jiayan'
	return queryTheAccession's all lines.
	'''
	    
	family_path = 'nt_%s'%(ntVirusesFamilyName)
	family_file_name = 'nt_%s.fasta'%(ntVirusesFamilyName)

	nt_viruses_family_path = blastDB_path+family_path
	nt_viruses_family_file = os.path.join(nt_viruses_family_path,family_file_name)

	accession_length = nt_filter_target_accessionLength(nt_viruses_family_file,queryTheAccession)
	#print accession_length

	query_blastn_file = target_blastn_query_file(querySample,blastnColumn)
	#print query_blastn_file
	with open(query_blastn_file,'r') as query_blastn_file_obj:
		queryLinesList = query_blastn_file_obj.readlines()
		#print queryLinesList  #['NODE_1_length_33877_cov_26.581575\tKJ883521.1\t99.917\t33907\t23\t5\t1\t33907\t108\t34009\t0.0\t62489\n',...
		
		target_identity_list = []
		target_length_list = []
		target_refStartPos_list = []
		target_refEndPos_list = []
		for i in range(len(queryLinesList)):
			accession = queryLinesList[i].split('\t')[1]
			if queryTheAccession == accession:
				identity = queryLinesList[i].split('\t')[2]
				length = queryLinesList[i].split('\t')[3]
				refStart = queryLinesList[i].split('\t')[8]
				refEnd = queryLinesList[i].split('\t')[9]
				refStartPos = min([refStart,refEnd])
				refEndPos = max([refStart,refEnd])
				target_identity_list.append(identity)
				target_length_list.append(length)
				target_refStartPos_list.append(refStartPos)
				target_refEndPos_list.append(refEndPos)
		'''
		print target_identity_list
		print target_length_list
		print target_refStartPos_list
		print target_refEndPos_list
		'''

		#fig = figure(figsize=(10,4),dpi=80)
		fig,ax = subplots(figsize=(10,2))
		hlines(0,0,accession_length,color='skyblue',linewidth=10.0)
		for i in range(len(target_length_list)):
			hlines(0.2,int(target_refStartPos_list[i]),int(target_refEndPos_list[i]),color='r',linewidth=4.0)
		title_str = "%s contigs with mapping aginst %s"%(querySample,queryTheAccession)
		title(title_str,fontsize=14)
		subplots_adjust(bottom=0.2,top=0.8)
		ax.spines['top'].set_visible(False)
		ax.spines['left'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.set_yticks([])  #no visible the y ticks

		output_path = blast_contigs_againt_ref_path + '/' + querySample		
		if not os.path.exists(output_path):
			os.system('mkdir %s'%output_path)
		fig_file = os.path.join(output_path,queryTheAccession+'_contigs.png')
		#print fig_file
		fig.savefig(fig_file)
		show()
