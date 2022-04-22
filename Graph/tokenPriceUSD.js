const csvwriter = require('csv-writer')
const axios = require('axios');
const prompt = require('prompt-sync')();

const func = async (tokenID, days) => {
	add = tokenID
	num_days = days
	try{
		const result = await axios.post(
			"https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
			{
				query: 
				`
				{
				 	tokenDayDatas(first: ${num_days}, orderBy: date, orderDirection: desc, 
				 		where: {
				 			token: "${add}"
				 		}
				 	)
				 	{
					        date
				 			priceUSD
				}
				}
				`
			} 
	);

		var createCsvWriter = csvwriter.createObjectCsvWriter
		const csvWriter = createCsvWriter({
  
			path: `data/prices/${add}.csv`,
			header: [
		  
			    {id: 'date', title: 'date'},
			    {id: 'priceUSD', title: 'priceUSD'},

			]
		});
		csvWriter
			.writeRecords(result.data.data.tokenDayDatas)
			.then(()=> console.log('Data uploaded into csv successfully'));

		console.log(result.data.data.tokenDayDatas);

	}	catch(error){
		console.error(error);

	}
}

func(process.argv[2], process.argv[3]);