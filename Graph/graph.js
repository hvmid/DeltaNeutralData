const csvwriter = require('csv-writer')
const axios = require('axios');

const main = async () => {
	try{
		const result = await axios.post(
			"https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
			{
				query: `
				{
				 	pairDayDatas(first: 365, orderBy: date, orderDirection: desc,
				   		where: {
				     		pairAddress: "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11",
				     		date_gt: 1592505859
				   		}
				 	) 
				 	{
					    date
					    dailyVolumeToken0
					    dailyVolumeToken1
					    dailyVolumeUSD
					    reserveUSD
				}
				}
				`
			} 
	);

		var createCsvWriter = csvwriter.createObjectCsvWriter
		const csvWriter = createCsvWriter({
  
			path: 'data.csv',
			header: [
		  
			    {id: 'date', title: 'date'},
			    {id: 'dailyVolumeToken0', title: 'dailyVolumeToken0'},
			    {id: 'dailyVolumeToken1', title: 'dailyVolumeToken1'},
			    {id: 'dailyVolumeUSD', title: 'dailyVolumeUSD'},
			    {id: 'reserveUSD', title: 'reserveUSD'}
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

main();