import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'environments/environment';

@Component({
  selector: 'app-multiclassification',
  templateUrl: './multiclassification.component.html',
  styleUrls: ['./multiclassification.component.css']
})
export class MulticlassificationComponent implements OnInit {
  rawDataset: Object={data:[]};
  columns:Array<string>=[]

  constructor(private http:HttpClient) { }

 async ngOnInit() {
    const httpOption = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }
    this.rawDataset = await this.http.get(environment.nodeApi + '/getMultiClassificationWithEngineId', httpOption).toPromise();
    this.columns = Object.keys(this.rawDataset['data'][0]);
    console.log(this.columns)
  }

}
