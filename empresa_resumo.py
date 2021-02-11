import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
plt.style.use('ggplot')

def read_data():
	data =  pd.read_csv('viagens.csv')

	del data['Unnamed: 0']

	return data

def companies_travels_delay_notTravels(data):
	
	#Dicionário no formado {empresa: [num. de viagens 'ida'+'volta']}
	companies_travels = {}

	#Dicionário no formado {empresa: atraso acumulado em minutos}
	companies_delays = {}

	#Dicionário no formado {empresa: quantidade de viagens não realizadas}
	companies_not_travels = {}

	for i in range(len(data['empresa'].values)):
		
		current_company = data['empresa'][i]
		
		#verifica se a chave já existe no dicionário. Se não existe, adiciona.
		if not current_company in companies_travels:
			companies_travels[current_company] = 0
			companies_delays[current_company] = []
			companies_not_travels[current_company] = 0

		#Contabiliza a viagem
		companies_travels[current_company] += 1

		#Se data['duracao_realizada'][i] é NaN, a condição do IF se torna falsa, e portanto não entra no IF.
		if data['duracao_prevista'][i] < data['duracao_realizada'][i]:
			companies_delays[current_company].append(data['duracao_realizada'][i]-data['duracao_prevista'][i])

		#Se data['duracao_realizada'][i] é NaN, a condição do IF se torna falsa, e portanto não entra no IF.
		if pd.isna(data['duracao_realizada'][i]):
			companies_not_travels[current_company] += 1

	return companies_travels,companies_delays,companies_not_travels

def transform_to_percent(companies_travels,companies_not_travels):

	for companie in companies_travels:
		companies_not_travels[companie] = companies_not_travels[companie]/companies_travels[companie]

	return companies_travels,companies_not_travels

def plot_delays_companies(companies_delays):

	total_delays = list(companies_delays.values())

	plt.title("Atraso acumulado por empresa",fontsize=20)
	handles = plt.bar(companies_delays.keys(),[sum(total_delays[i])/60 for i in range(len(total_delays))],width=0.5,color=['black','green','blue','orange'])
	plt.ylabel("Horas",fontsize=20)
	plt.xticks([])
	plt.yticks(fontsize=20)
	plt.legend(handles=handles,labels=companies_delays.keys(),fontsize=10)
	#plt.show()

def plot_travels_companies(companies_travels):

	plt.title("Quantidade de viagens por empresa\nIda+Volta",fontsize=20)
	handles = plt.bar(companies_travels.keys(),companies_travels.values(),width=0.5,color=['black','green','blue','orange'])
	plt.ylabel("Quantidade\nde viagens",fontsize=20)
	plt.xticks([])
	plt.yticks(fontsize=20)
	plt.legend(handles=handles,labels=companies_travels.keys(),fontsize=10)
	#plt.show()

def plot_not_travels(companies_not_travels):

	plt.title("Quantidade de viagens não realizadas",fontsize=20)
	handles = plt.bar(companies_not_travels.keys(),companies_not_travels.values(),width=0.5,color=['black','green','blue','orange'])
	plt.ylabel("Porcentagem",fontsize=20)
	plt.xticks([])
	plt.yticks(fontsize=20)
	plt.legend(handles=handles,labels=companies_not_travels.keys(),fontsize=10)
	#plt.show()

def plot_median_delays(companies_delays):

	mean_delays = {}
	
	for company in companies_delays:
		mean_delays[company] = np.median(companies_delays[company])

	
	plt.title("Atraso mediano por viagem",fontsize=20)
	handles = plt.bar(mean_delays.keys(),mean_delays.values(),width=0.5,color=['black','green','blue','orange'])
	plt.ylabel("Minutos",fontsize=20)
	plt.xticks([])
	plt.yticks(fontsize=20)
	plt.legend(handles=handles,labels=mean_delays.keys(),fontsize=10)


def plot_mean_delays(companies_delays):

	mean_delays = {}
	std_delays = {}

	
	for company in companies_delays:
		mean_delays[company] = np.mean(companies_delays[company])

	
	plt.title("Atraso médio por viagem",fontsize=20)
	handles = plt.bar(mean_delays.keys(),mean_delays.values(),width=0.5,color=['black','green','blue','orange'])
	plt.ylabel("Minutos",fontsize=20)
	plt.xticks([])
	plt.yticks(fontsize=20)
	plt.legend(handles=handles,labels=mean_delays.keys(),fontsize=10)
	

def plot_boxplot_delays(companies_delays):
	

	plt.title('Box plot dos atrasos\npor empresa')
	plt.boxplot([companies_delays[company] for company in companies_delays],labels=[list(companies_delays.keys())[i].split(' ')[0] for i in range(len(companies_delays)) ] )
	plt.xlabel('Primeiro nome da empresa',fontsize=20)
	plt.xticks(fontsize=15)

	plt.ylabel('Minutos',fontsize=20)
	plt.yticks(fontsize=15)

def review_company(data):


	companies_travels,companies_delays,companies_not_travels = companies_travels_delay_notTravels(data)
	plt.subplot(321)
	plot_travels_companies(companies_travels)

	plt.subplot(322)
	plot_delays_companies(companies_delays)

	companies_travels,companies_not_travels = transform_to_percent(companies_travels,companies_not_travels)
	plt.subplot(323)
	plot_not_travels(companies_not_travels)

	plt.subplot(324)
	plot_mean_delays(companies_delays)

	plt.subplot(325)
	plot_boxplot_delays(companies_delays)

	plt.subplot(326)
	plot_median_delays(companies_delays)

	plt.show()


def main():
	data = read_data()
	review_company(data)

main()


