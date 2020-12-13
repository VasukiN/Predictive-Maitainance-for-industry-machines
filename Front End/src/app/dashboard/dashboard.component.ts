import { Component, OnInit } from '@angular/core';
import * as Chartist from 'chartist';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'environments/environment';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})


export class DashboardComponent implements OnInit {

  rawDataset: Object={data:[]};
  rul_regression_key:Array<string>=[]
  rul_regression_value:Array<number>=[]

  binaryClassification_Dataset: Object={data:[]};
  binary_classification_key:Array<string>=[]
  binary_classification_value:Array<number>=[]

  multiClassification_Dataset: Object={data:[]};
  multi_classification_key:Array<string>=[]
  multi_classification_value:Array<number>=[]

  binaryClassification_Count_Dataset: Object={data:[]};
  binary_classification_count_key:Array<string>=[]
  binary_classification_count_value:Array<number>=[]
  binary_classification_count_value_eachset:Array<number>=[]

  multiClassification_Count_Dataset: Object={data:[]};
  multi_classification_count_key:Array<string>=[]
  multi_classification_count_value:Array<number>=[]
  multi_classification_count_value_eachset:Array<number>=[]


  rul_by_regression_engineId_lessthan30_Dataset: Object={data:[]};
  rul_by_regression_engineId_lessthan30_count:number;

  //currentCustomer = 'Maria';
  
  constructor(private http:HttpClient) { }

  
  startAnimationForLineChart(chart){
      let seq: any, delays: any, durations: any;
      seq = 0;
      delays = 80;
      durations = 500;

      chart.on('draw', function(data) {
        if(data.type === 'line' || data.type === 'area') {
          data.element.animate({
            d: {
              begin: 600,
              dur: 700,
              from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
              to: data.path.clone().stringify(),
              easing: Chartist.Svg.Easing.easeOutQuint
            }
          });
        } else if(data.type === 'point') {
              seq++;
              data.element.animate({
                opacity: {
                  begin: seq * delays,
                  dur: durations,
                  from: 0,
                  to: 1,
                  easing: 'ease'
                }
              });
          }
      });

      seq = 0;
  };
  startAnimationForBarChart(chart){
      let seq2: any, delays2: any, durations2: any;

      seq2 = 0;
      delays2 = 80;
      durations2 = 500;
      chart.on('draw', function(data) {
        if(data.type === 'bar'){
            seq2++;
            data.element.animate({
              opacity: {
                begin: seq2 * delays2,
                dur: durations2,
                from: 0,
                to: 1,
                easing: 'ease'
              }
            });
        }
      });

      seq2 = 0;
  };
  async ngOnInit() {
      const httpOption = {
        headers: new HttpHeaders({
          'Content-Type': 'application/json'
        })
      }
      this.rawDataset = await this.http.get(environment.nodeApi + '/getMseOfRulByRegressionWithEngineId', httpOption).toPromise();
      this.rul_regression_key = Object.keys(this.rawDataset['data']);
       this.rul_regression_value = Object.values(this.rawDataset['data']);
      // console.log(this.rul_regression_key)
      // console.log(this.rul_regression_value)

      this.binaryClassification_Dataset = await this.http.get(environment.nodeApi + '/getAccuracyOfBinaryClassificationWithEngineId', httpOption).toPromise();
      this.binary_classification_key = Object.keys(this.binaryClassification_Dataset['data']);
      this.binary_classification_value = Object.values(this.binaryClassification_Dataset['data']);
      // console.log(this.rul_regression_key)
      // console.log(this.rul_regression_value)

      this.multiClassification_Dataset = await this.http.get(environment.nodeApi + '/getAccuracyOfMultiClassificationWithEngineId', httpOption).toPromise();
      this.multi_classification_key = Object.keys(this.multiClassification_Dataset['data']);

      // this.multi_classification_value = Object.keys(this.multiClassification_Dataset['data']).map(a=>a)
      this.multi_classification_value = Object.values(this.multiClassification_Dataset['data']);
      // console.log(this.rul_regression_key)
      // console.log(this.rul_regression_value)

      this.binaryClassification_Count_Dataset = await this.http.get(environment.nodeApi + '/getCountOfBinaryClassificationWithEngineId', httpOption).toPromise();
      //this.binary_classification_count_key = Object.keys(this.binaryClassification_Count_Dataset['data']);
       //this.binary_classification_count_value = Object.values(this.binaryClassification_Count_Dataset['data']);
      // console.log(this.binary_classification_count_key)
      // console.log(this.binary_classification_count_value)
      this.binary_classification_count_value_eachset = this.binaryClassification_Count_Dataset['data'];
      // console.log(this.binary_classification_count_value_eachset)

      this.multiClassification_Count_Dataset = await this.http.get(environment.nodeApi + '/getCountOfMultiClassificationWithEngineId', httpOption).toPromise();
     // this.multi_classification_count_key = Object.keys(this.multiClassification_Count_Dataset['data']);
      //this.multi_classification_count_value = Object.values(this.multiClassification_Count_Dataset['data']);
      this.multi_classification_count_value_eachset =  this.multiClassification_Count_Dataset['data'];
      //console.log(this.multi_classification_count_key)
      //console.log(this.multi_classification_count_value)


      
      this.rul_by_regression_engineId_lessthan30_Dataset = await this.http.get(environment.nodeApi + '/getRulByRegressionWithEngineIdCountLessthan30', httpOption).toPromise();
     // this.multi_classification_count_key = Object.keys(this.multiClassification_Count_Dataset['data']);
     // this.multi_classification_count_value = Object.values(this.multiClassification_Count_Dataset['data']);
      this.rul_by_regression_engineId_lessthan30_count =  this.rul_by_regression_engineId_lessthan30_Dataset['data'];
      // console.log(this.rul_by_regression_engineId_lessthan30_count)
      //this.currentCustomer = "current";

      //console.log("--------------------------------------")
      //console.log(this.rul_by_regression_engineId_lessthan30_Dataset)
     

      /* ----------==========     Daily Sales Chart initialization For Documentation    ==========---------- */

      const dataDailySalesChart: any = {
          // labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
          // series: [
          //     [12, 17, 7, 17, 23, 18, 38]
          // ]
          labels: this.binary_classification_key,
          series: [
            this.binary_classification_value
          ]
      };

     const optionsDailySalesChart: any = {
          lineSmooth: Chartist.Interpolation.cardinal({
              tension: 0
          }),
          axisY: {
            offset: 100
          },
          //low: 0,
          //high: 50, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          low:0.5,
          high: 1,
          horizontalBars: true,
          chartPadding: { top: 0, right: 0, bottom: 0, left: 0},
      }

      //var dailySalesChart = new Chartist.Line('#dailySalesChart', dataDailySalesChart, optionsDailySalesChart);
      var dailySalesChart = new Chartist.Bar('#dailySalesChart', dataDailySalesChart, optionsDailySalesChart);

      this.startAnimationForLineChart(dailySalesChart);


      /* ----------==========     Completed Tasks Chart initialization    ==========---------- */

      const dataCompletedTasksChart: any = {
          // labels: ['12p', '3p', '6p', '9p', '12p', '3a', '6a', '9a'],
          // series: [
          //     [230, 750, 450, 300, 280, 240, 200, 190]
          // ]
          labels: this.multi_classification_key,
          series: [
            this.multi_classification_value
          ]
      };

     const optionsCompletedTasksChart: any = {
          lineSmooth: Chartist.Interpolation.cardinal({
              tension: 0
          }),
          axisY: {
            offset: 100
          },
          // low: 0,
          // high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          low:0.5,
          high: 1,
          horizontalBars: true,
          chartPadding: { top: 0, right: 0, bottom: 0, left: 0}
      }

      //var completedTasksChart = new Chartist.Line('#completedTasksChart', dataCompletedTasksChart, optionsCompletedTasksChart);
      var completedTasksChart = new Chartist.Bar('#completedTasksChart', dataCompletedTasksChart, optionsCompletedTasksChart);

      // start animation for the Completed Tasks Chart - Line Chart
      this.startAnimationForLineChart(completedTasksChart);



      /* ----------==========     Emails Subscription Chart initialization    ==========---------- */

      var datawebsiteViewsChart = {
        // labels: ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
        // series: [
        //   [542, 443, 320, 780, 553, 453, 326, 434, 568, 610, 756, 895]

        // ]
        labels: this.rul_regression_key,
        series: [this.rul_regression_value]
      };

      var optionswebsiteViewsChart = {
          axisX: {
              showGrid: false
          },
          axisY: {
            offset: 100
          },
          // low: 0,
          // high: 1000,
          low: 500,
          high: 1500,
          horizontalBars: true,
          chartPadding: { top: 0, right: 0, bottom: 0, left: 0}
      };
      var responsiveOptions: any[] = [
        ['screen and (max-width: 640px)', {
          seriesBarDistance: 5,
          axisX: {
            labelInterpolationFnc: function (value) {
              return value[0];
            }
          }
        }]
      ];
      var websiteViewsChart = new Chartist.Bar('#websiteViewsChart', datawebsiteViewsChart, optionswebsiteViewsChart, responsiveOptions);

      //start animation for the Emails Subscription Chart
      this.startAnimationForBarChart(websiteViewsChart);
  }

}

