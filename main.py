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

		if not current_company in companies_delays:
			companies_delays[current_company] = 0

		if not current_company in companies_not_travels:
			companies_not_travels[current_company] = 0

		#Contabiliza a viagem
		companies_travels[current_company] += 1

		#Se data['duracao_realizada'][i] é NaN, a condição do IF se torna falsa, e portanto não entra no IF.
		if data['duracao_prevista'][i] < data['duracao_realizada'][i]:
			companies_delays[current_company] += (data['duracao_realizada'][i]-data['duracao_prevista'][i])/60

		#Se data['duracao_realizada'][i] é NaN, a condição do IF se torna falsa, e portanto não entra no IF.
		if pd.isna(data['duracao_realizada'][i]):
			companies_not_travels[current_company] += 1

	return companies_travels,companies_delays,companies_not_travels

def transform_to_percent(companies_travels,companies_not_travels):

	for companie in companies_travels:
		companies_not_travels[companie] = companies_not_travels[companie]/companies_travels[companie]

	return companies_travels,companies_not_travels

def plot_delays_companies(companies_delays):

	plt.title("Atraso acumulado por empresa",fontsize=20)
	handles = plt.bar(companies_delays.keys(),companies_delays.values(),width=0.5,color=['black','green','blue','orange'])
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

def review_company(data):


	companies_travels,companies_delays,companies_not_travels = companies_travels_delay_notTravels(data)
	plt.subplot(221)
	plot_travels_companies(companies_travels)

	plt.subplot(222)
	plot_delays_companies(companies_delays)

	companies_travels,companies_not_travels = transform_to_percent(companies_travels,companies_not_travels)
	plt.subplot(223)
	plot_not_travels(companies_not_travels)

	plt.show()

#---------------------------------------------------------------------------------


def legend_without_duplicate_labels(ax):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique))

def line_delay(data,top):
	
	#Dicionário no formado {num. da linha: atraso acumulado}
	lines_delay = {}

	#Dicionário no formado {num. da linha: empresa responsável}
	lines_company = {}

	#Dicionario no formato {empresa:[cor,flag para indicar se ja foi usado]}. Será útil para plotar o gráfico depois.
	companies = {}
	

	for i in range(len(data['numero_linha'].values)):
		
		current_line = str(data['numero_linha'][i])
		current_company = data['empresa'][i]
		
		#Se data['duracao_realizada'][i] é NaN, a condição do IF se torna falsa, e portanto não entra no IF.
		if data['duracao_prevista'][i] < data['duracao_realizada'][i]:

			#verifica se a chave já existe no dicionário. Se não existe, adiciona.
			if not current_line in lines_delay:
				lines_delay[current_line] = 0

			#verifica se a chave já existe no dicionário. Se não existe, adiciona.
			if not current_line in lines_company:
				lines_company[current_line] = current_company

			if not current_company in companies:
				companies[current_company] = [(random.random(),random.random(),random.random()),False] #Cor em RGB

			lines_delay[current_line] += (data['duracao_realizada'][i]-data['duracao_prevista'][i])/60


	lines_order = sorted(lines_delay,key=lines_delay.get)
	delay_order = sorted(lines_delay.values())
	company_order = [lines_company[x] for x in lines_order]

	company_order.reverse()
	lines_order.reverse()
	delay_order.reverse()

	plt.subplot(121)

	if top == -1:
		plt.title("Atraso por linha\nIda+Volta",fontsize=20)
		top = len(lines_order)
	else:
		plt.title("(TOP "+str(top)+")\nAtraso por linha\nIda+Volta",fontsize=20)

	handles = plt.bar(lines_order[:top],delay_order[:top],width=0.5)
	
	#Loop para remover legendas duplicadas no gráfico.
	filter_handles = []
	colors = []
	for i in range(len(handles)):
		
		#Se é a primeira vez que a empresa vai apareer no gráfico, então a gente filtra, pra depois não aparecer legenda repetida
		if not companies[company_order[i]][1]:
			companies[company_order[i]][1] = True
			filter_handles.append(i)
			colors.append(companies[company_order[i]][0])
		handles[i].set_color(companies[company_order[i]][0])



	plt.ylabel("Horas",fontsize=20)
	plt.xticks(rotation='vertical')
	plt.yticks(fontsize=20)

	plt.legend(handles=[handles[x] for x in filter_handles],labels=[company_order[x] for x in filter_handles],fontsize=10)
	#plt.show()
	plt.subplot(122)

	#dicionário no formato {empresa: quantidade de vezes que aparece no pódio}
	top_companies = {}

	for i in range(top):
		if not company_order[i] in top_companies:
			top_companies[company_order[i]] = 0

		top_companies[company_order[i]] += 1

	plt.pie(x = top_companies.values(),labels=top_companies.keys(),autopct='%1.1f%%',
        shadow=True, startangle=90,colors=colors)
	plt.show()
	
def review_line_perDelay(data):
	top = int(input("Tamanho do pódio (-1 se máximo): "))
	line_delay(data,top)



def main():
	data = read_data()
	
	while True:

		option = int(input("1. Resumo de acordo com a empresa\n2. Resumo de acordo com atrasos\nEscolha sua opção: "))
		
		if option == 1:
			review_company(data)
		else:
			review_line_perDelay(data)

main()


