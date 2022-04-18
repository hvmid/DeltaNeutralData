const csvwriter = require('csv-writer')
const axios = require('axios');

const main = async (top) => {
	try{
		const result = await axios.post(
			"https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
			{
				query: 
				`
				{
				 	pairDayDatas(first: ${top}, orderBy: reserveUSD, orderDirection: desc, where: {date: 1650153600}
				 	) 
				 	{
				 			token0{
				 				symbol
				 			}
				 			token1{
				 				symbol
				 			}
						    reserveUSD
						    pairAddress

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
			    {id: 'reserveUSD', title: 'reserveUSD'},
			    {id: 'pairAddress', title: 'pairAddress'},
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

main(process.argv[2]);