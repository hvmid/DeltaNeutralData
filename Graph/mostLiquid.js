const csvwriter = require('csv-writer')
const axios = require('axios');

const main = async (top, date) => {
	try{
		const result = await axios.post(
			"https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
			{
				query: 
				`
				{
				 	pairDayDatas(first: ${top}, orderBy: reserveUSD, orderDirection: desc, 
				 		where: {
				 			date: ${date}}){,
				 			token0{
				 				symbol
				 			}
				 			token1{
				 				symbol
				 			}
				 			pairAddress
						    reserveUSD
						    dailyVolumeUSD
				}
				}
				`
			} 
	);

		var createCsvWriter = csvwriter.createObjectCsvWriter
		const csvWriter = createCsvWriter({
  
			path: 'topPairs.csv',
			headerIdDelimiter: '.',
			header: [
				{id: 'token0.symbol', title: 'token0'},
				{id: 'token1.symbol', title: 'token1'},
			    {id: 'pairAddress', title: 'pairAddress'},
			    {id: 'reserveUSD', title: 'reserveUSD'},
			    {id: 'dailyVolumeUSD', title: 'dailyVolumeUSD'},
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

main(process.argv[2], process.argv[3]);