import { Component, OnInit} from '@angular/core';
import { ApiService } from '../../api.service';

@Component({
  selector: 'app-card2',
  templateUrl: './card2.component.html',
  styleUrls: ['./card2.component.css'],
  providers : [ApiService]
})
export class Card2Component implements OnInit {

  total_fraud: any
  total_confirme : any
  last_date: any
  next_date : any
  total_frauds_last_date : any
  n_fraud_region: any 
  n_fraud_region_graph : any
  constructor(private api:  ApiService) {
    this.getDataCards();
   }

  ngOnInit() {}

  getDataCards = () => {
    this.api.getDataCards().subscribe(
      data => {
        this.total_fraud            = data.total
        this.total_confirme         = data.confirme
        this.last_date              = data.last_date
        this.next_date              = data.next_date
        this.total_frauds_last_date = data.total_last_date
        console.log(data)
      },
      error => {
        console.log(error)
      }
    )
  }
}
