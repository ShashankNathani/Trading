const access_key = "dac353010695a844a5eb76fc2d197f82";

function average(data){
    var sum = 0;
    for(var i = 0; i < data.length; i++){
        sum += data[i];
    }

    return sum/data.length;
}

function moving_window_average_return(data,window_size){
    
    if(data.length < window_size){
        return window.dash_clientside.no_update ;
    }// Do something with the data

    let moving_window = [];
    for(let i = 0; i < (data.length - window_size); i++){
        moving_window.push((data[i+window_size]/data[i])-1);
    }
    console.log(moving_window);
    return average(moving_window);
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clients: {
        get_api_data : async function(ticker){
            
            if (ticker == null || ticker == "") {
                console.log("No ticker provided");
                return null;
            }

            var sym = ticker.split(" ")[0];
            var start = '2015-01-01';
            var end = new Date().toISOString().split('T')[0];
            var url = `http://api.marketstack.com/v1/eod?access_key=${access_key}&symbols=${sym}&date_from=${start}&date_to=${end}&sort=ASC&limit=1000`;
            const options = {
                method: "GET",
            };
            
            try {
                const response = await fetch(url, options);
                var result = await response.text();
            } catch (error) {
                console.error(error);
            }
            return JSON.parse(result);
        },

        get_adjusted_close_average : function(api_data,start_date,end_date,window_size){
            let data = [];
            for(var i = 0; i < api_data['data'].length; i++){
                date = api_data['data'][i]['date'];
                if(date < start_date || date > end_date){
                    continue;
                }
                adj_close = api_data['data'][i]['adj_close'];
                data.push(adj_close);
            }
            
            return moving_window_average_return(data,window_size);

        }
    }
});