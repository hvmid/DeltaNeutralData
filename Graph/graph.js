const csvwriter = require('csv-writer')
const axios = require('axios');
const prompt = require('prompt-sync')();

const func = async (pairadd) => {
	pairad = pairadd
	try{
		const result = await axios.post(
			"https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
			{
				query: 
				`
				{
				 	pairDayDatas(first: 365, orderBy: date, orderDirection: desc,
				   		where: {
				     		pairAddress: "${pairad}",
				     		date_gt: 1592505859
				   		}
				 	) 
				 	{
					        date
						  	reserve0
						  	reserve1
						    totalSupply
						    reserveUSD
						  	dailyVolumeToken0
						  	dailyVolumeToken1
						    dailyVolumeUSD
						  	dailyTxns
				}
				}
				`
			} 
	);

		var createCsvWriter = csvwriter.createObjectCsvWriter
		const csvWriter = createCsvWriter({
  
			path: `data/${pairad}.csv`,
			header: [
		  
			    {id: 'date', title: 'date'},
			    {id: 'reserve0', title: 'reserve0'},
			    {id: 'reserve1', title: 'reserve1'},
			    {id: 'totalSupply', title: 'totalSupply'},
			    {id: 'reserveUSD', title: 'reserveUSD'},
			    {id: 'dailyVolumeToken0', title: 'dailyVolumeToken0'},
			    {id: 'dailyVolumeToken1', title: 'dailyVolumeToken1'},
			    {id: 'dailyVolumeUSD', title: 'dailyVolumeUSD'},
			    {id: 'dailyTxns', title: 'dailyTxns'},
			    
			]
		});
		csvWriter
			.writeRecords(result.data.data.pairDayDatas)
			.then(()=> console.log('Data uploaded into csv successfully'));

		console.log(result.data.data.pairDayDatas);

	}	catch(error){
		console.error(error);

	}
}

func(process.argv[2]);