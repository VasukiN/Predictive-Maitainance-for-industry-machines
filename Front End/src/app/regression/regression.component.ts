// import { Component, OnInit } from '@angular/core';

// @Component({
//   selector: 'app-regression',
//   templateUrl: './regression.component.html',
//   styleUrls: ['./regression.component.css']
// })
// export class RegressionComponent implements OnInit {

//   constructor() { }

//   ngOnInit(): void {
//   }

// }
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { environment } from 'environments/environment';

@Component({
  selector: 'app-regressor-unit',
  templateUrl: './regression.component.html',
  styleUrls: ['./regression.component.css']
})
export class RegressionComponent implements OnInit {
  rawDataset: Object={data:[]};
  columns:Array<string>=[]

  
  constructor(private http:HttpClient) { }

 async ngOnInit() {
    const httpOption = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }
    this.rawDataset = await this.http.get(environment.nodeApi + '/getRulByRegressionWithEngineId', httpOption).toPromise();
    this.columns = Object.keys(this.rawDataset['data'][0]);
  }

}