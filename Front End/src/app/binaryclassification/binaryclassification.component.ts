import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'environments/environment';

@Component({
  selector: 'app-binaryclassification',
  templateUrl: './binaryclassification.component.html',
  styleUrls: ['./binaryclassification.component.css']
})
export class BinaryclassificationComponent implements OnInit {

   rawDataset: Object={data:[]};
  columns:Array<string>=[]

  constructor(private http:HttpClient) { }

 async ngOnInit() {
    const httpOption = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }
    this.rawDataset = await this.http.get(environment.nodeApi + '/getBinaryClassificationWithEngineId', httpOption).toPromise();
    this.columns = Object.keys(this.rawDataset['data'][0]);
  }
}
