let count = 0;
if (document.getElementById('top_x_div2')){
    count=2;
    //console.log(count)
}
if (document.getElementById('top_x_div3')){
    count=0;
    //console.log(count)
}
if (document.getElementById('top_x_div1')){
    count=1;
    //console.log(count)
}

function myFunction(){
    count++;
    console.log(count);
    if (count%2 ==0){
        document.getElementById("top_x_div1").id = "top_x_div2";
        var allGames = [];
        var useless = 0;
        //default
        var bestGame = [];
        var secondBestGame = ["-","now",0,'-'];
        var thirdBestGame = ["-","now",0,'-'];
        var fourthBestGame = ["-","now",0,'-'];
        var fifthBestGame = ["-","now",0,'-'];


        function showTableData() {
            var myTab = document.getElementById('insidetable');

            for (i = 1; i < myTab.rows.length; i++) {
                // GET THE CELLS COLLECTION OF THE CURRENT ROW.
                var objCells = myTab.rows.item(i).cells;
                var game =[];
                var k=1;
                // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
                for (var j = 2; j < objCells.length; j++) {
                    if(objCells.item(2).innerHTML.localeCompare('medium ')!=0){
                        useless++;
                        k=0;
                        break;
                    }
                    if(j==4){
                        var x = Number(objCells.item(j).innerHTML);
                        game.push(x);
                    }
                    else{
                        game.push(objCells.item(j).innerHTML);
                    }
                }
                if(k!=0){
                    allGames.push(game);
                }
            }

            allGames.sort(function(a,b) { // sort based on the score
                return a[2]-b[2]
            });

            console.log(myTab.rows.length);
            console.log(allGames);
            bestGame.push(allGames[myTab.rows.length-useless-2]);
            
            if(myTab.rows.length-useless >= 3){
                secondBestGame =[];
                secondBestGame.push(allGames[myTab.rows.length-useless-3]);
            }
            if(myTab.rows.length-useless >= 4){
                thirdBestGame =[];
                thirdBestGame.push(allGames[myTab.rows.length-useless-4]);
            }
            if(myTab.rows.length-useless >= 5){
                fourthBestGame =[];
                fourthBestGame.push(allGames[myTab.rows.length-useless-5]);
            }
            if(myTab.rows.length-useless >= 6){
                fifthBestGame =[];
                fifthBestGame.push(allGames[myTab.rows.length-useless-6]);
            }
        }

        showTableData();
        google.charts.load("current", {'packages':['bar']});
        google.charts.setOnLoadCallback(drawStuff);

        function drawStuff() {
            var data = new google.visualization.arrayToDataTable([
                ['Time', 'Score'],
                [bestGame[0][3], bestGame[0][2]],
                [secondBestGame[0][3], secondBestGame[0][2]],
                [thirdBestGame[0][3], thirdBestGame[0][2]],
                [fourthBestGame[0][3], fourthBestGame[0][2]],
                [fifthBestGame[0][3], fifthBestGame[0][2]]
            ]);

            var options = {
                bar: {groupWidth: "60%"},
                title: 'Your Top 5 games - difficulty:  MEDIUM',
                colors: ['#09b4b9'],
                width: 700,
                height: 350,
                animation:{
                    "startup": true,
                    duration: 2000,
                    easing: 'out'
                },
                backgroundColor: {fill:'transparent'},
                legend: { position: 'none' },
                chart: { title: 'Your Top 5 games - difficulty:  MEDIUM'},
                bars: 'vertical', // Required for Material Bar Charts.
                axes: {
                y: {
                    0: { side: 'top', label: 'Score'} // Top x-axis.
                }
                },
                hAxis: {
                    textStyle:{color: 'white'}
                },
                vAxis: {
                    textStyle:{color: 'white'}
                },
                titleTextStyle: {
                    color: 'rgb(201, 204, 6)',
                    fontSize: 15, 
                }
            };

            var chart = new google.charts.Bar(document.getElementById('top_x_div2'));
            chart.draw(data, google.charts.Bar.convertOptions(options));
            google.visualization.events.addListener(chart, 'ready', () => {
                setTimeout(() => {
                    document.getElementById('top_x_div2').classList.remove('animated-chart-start')
                }, 1000)
            });
        }
    }
    else if(count%3==0){
        document.getElementById("top_x_div2").id = "top_x_div3";
        var allGames = [];
        var useless = 0;
        //default
        var bestGame = [];
        var secondBestGame = ["-","now",0,'-'];
        var thirdBestGame = ["-","now",0,'-'];
        var fourthBestGame = ["-","now",0,'-'];
        var fifthBestGame = ["-","now",0,'-'];


        function showTableData() {
            var myTab = document.getElementById('insidetable');

            for (i = 1; i < myTab.rows.length; i++) {
                // GET THE CELLS COLLECTION OF THE CURRENT ROW.
                var objCells = myTab.rows.item(i).cells;
                var game =[];
                var k=1;
                // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
                for (var j = 2; j < objCells.length; j++) {
                    if(objCells.item(2).innerHTML.localeCompare('hard ')!=0){
                        useless++;
                        k=0;
                        break;
                    }
                    if(j==4){
                        var x = Number(objCells.item(j).innerHTML);
                        game.push(x);
                    }
                    else{
                        game.push(objCells.item(j).innerHTML);
                    }
                }
                if(k!=0){
                    allGames.push(game);
                }
            }

            allGames.sort(function(a,b) { // sort based on the score
                return a[2]-b[2]
            });

            console.log(myTab.rows.length);
            console.log(allGames);
            bestGame.push(allGames[myTab.rows.length-useless-2]);
            
            if(myTab.rows.length-useless >= 3){
                secondBestGame =[];
                secondBestGame.push(allGames[myTab.rows.length-useless-3]);
            }
            if(myTab.rows.length-useless >= 4){
                thirdBestGame =[];
                thirdBestGame.push(allGames[myTab.rows.length-useless-4]);
            }
            if(myTab.rows.length-useless >= 5){
                fourthBestGame =[];
                fourthBestGame.push(allGames[myTab.rows.length-useless-5]);
            }
            if(myTab.rows.length-useless >= 6){
                fifthBestGame =[];
                fifthBestGame.push(allGames[myTab.rows.length-useless-6]);
            }
        }
        count = 0;
        console.log(count);
        showTableData();
        google.charts.load("current", {'packages':['bar']});
        google.charts.setOnLoadCallback(drawStuff);

        function drawStuff() {
            var data = new google.visualization.arrayToDataTable([
                ['Time', 'Score'],
                [bestGame[0][3], bestGame[0][2]],
                [secondBestGame[0][3], secondBestGame[0][2]],
                [thirdBestGame[0][3], thirdBestGame[0][2]],
                [fourthBestGame[0][3], fourthBestGame[0][2]],
                [fifthBestGame[0][3], fifthBestGame[0][2]]
            ]);

            var options = {
                bar: {groupWidth: "60%"},
                title: 'Your Top 5 games - difficulty:  HARD',
                colors: ['#09b4b9'],
                width: 700,
                height: 350,
                animation:{
                    "startup": true,
                    duration: 2000,
                    easing: 'out'
                },
                backgroundColor: {fill:'transparent'},
                legend: { position: 'none' },
                chart: { title: 'Your Top 5 games - difficulty:  HARD'},
                bars: 'vertical', // Required for Material Bar Charts.
                axes: {
                y: {
                    0: { side: 'top', label: 'Score'} // Top x-axis.
                }
                },
                hAxis: {
                    textStyle:{color: 'white'}
                },
                vAxis: {
                    textStyle:{color: 'white'}
                },
                titleTextStyle: {
                    color: 'FF4444',
                    fontSize: 15, 
                }
            };
            
            var chart = new google.charts.Bar(document.getElementById('top_x_div3'));
            chart.draw(data, google.charts.Bar.convertOptions(options));
            google.visualization.events.addListener(chart, 'ready', () => {
                setTimeout(() => {
                    document.getElementById('top_x_div3').classList.remove('animated-chart-start')
                }, 1000)
            });
        }
    }
    else{
        document.getElementById("top_x_div3").id = "top_x_div1";
        var allGames = [];
        var useless = 0;
        //default
        var bestGame = [];
        var secondBestGame = ["-","now",0,'-'];
        var thirdBestGame = ["-","now",0,'-'];
        var fourthBestGame = ["-","now",0,'-'];
        var fifthBestGame = ["-","now",0,'-'];


        function showTableData() {
            var myTab = document.getElementById('insidetable');

            for (i = 1; i < myTab.rows.length; i++) {
                // GET THE CELLS COLLECTION OF THE CURRENT ROW.
                var objCells = myTab.rows.item(i).cells;
                var game =[];
                var k=1;
                // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
                for (var j = 2; j < objCells.length; j++) {
                    if(objCells.item(2).innerHTML.localeCompare('easy ')!=0){
                        useless++;
                        k=0;
                        break;
                    }
                    if(j==4){
                        var x = Number(objCells.item(j).innerHTML);
                        game.push(x);
                    }
                    else{
                        game.push(objCells.item(j).innerHTML);
                    }
                }
                if(k!=0){
                    allGames.push(game);
                }
            }

            allGames.sort(function(a,b) { // sort based on the score
                return a[2]-b[2]
            });

            console.log(myTab.rows.length);
            console.log(allGames);
            bestGame.push(allGames[myTab.rows.length-useless-2]);
            
            if(myTab.rows.length-useless >= 3){
                secondBestGame =[];
                secondBestGame.push(allGames[myTab.rows.length-useless-3]);
            }
            if(myTab.rows.length-useless >= 4){
                thirdBestGame =[];
                thirdBestGame.push(allGames[myTab.rows.length-useless-4]);
            }
            if(myTab.rows.length-useless >= 5){
                fourthBestGame =[];
                fourthBestGame.push(allGames[myTab.rows.length-useless-5]);
            }
            if(myTab.rows.length-useless >= 6){
                fifthBestGame =[];
                fifthBestGame.push(allGames[myTab.rows.length-useless-6]);
            }
        }

        showTableData();
        google.charts.load("current", {'packages':['bar']});
        google.charts.setOnLoadCallback(drawStuff);

        function drawStuff() {
            var data = new google.visualization.arrayToDataTable([
                ['Time', 'Score'],
                [bestGame[0][3], bestGame[0][2]],
                [secondBestGame[0][3], secondBestGame[0][2]],
                [thirdBestGame[0][3], thirdBestGame[0][2]],
                [fourthBestGame[0][3], fourthBestGame[0][2]],
                [fifthBestGame[0][3], fifthBestGame[0][2]]
            ]);

            var options = {
                bar: {groupWidth: "60%"},
                title: 'Your Top 5 games - difficulty:  EASY',
                colors: ['#09b4b9'],
                width: 700,
                height: 350,
                animation:{
                    "startup": true,
                    duration: 2000,
                    easing: 'out'
                },
                backgroundColor: {fill:'transparent'},
                legend: { position: 'none' },
                chart: { title: 'Your Top 5 games - difficulty:  EASY'},
                bars: 'vertical', // Required for Material Bar Charts.
                axes: {
                y: {
                    0: { side: 'top', label: 'Score'} // Top x-axis.
                }
                },
                hAxis: {
                    textStyle:{color: 'white'}
                },
                vAxis: {
                    textStyle:{color: 'white'}
                },
                titleTextStyle: {
                    color: 'chartreuse',
                    fontSize: 15, 
                }
            };

            var chart = new google.charts.Bar(document.getElementById('top_x_div1'));
            chart.draw(data, google.charts.Bar.convertOptions(options));
            google.visualization.events.addListener(chart, 'ready', () => {
                setTimeout(() => {
                    document.getElementById('top_x_div1').classList.remove('animated-chart-start')
                }, 1000)
            });
        }
    }
};