import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }
  BASE_URL = "http://127.0.0.1:8000/"
  HTTP_HEADERS = new HttpHeaders({'Content-Type' : 'application/json'})

  getDataCards() : Observable<any> {
    return this.http.get(this.BASE_URL + "cards/", 
    {headers : this.HTTP_HEADERS})
  }

  fraudDetectedConfirmed() : Observable<any> {
    return this.http.get(this.BASE_URL + "frauddetectdconfrmed/", 
    {headers : this.HTTP_HEADERS})
  }

  fraudParRegion() : Observable<any> {
    return this.http.get(this.BASE_URL + "fraudparregion/", 
    {headers : this.HTTP_HEADERS})
  }

  fraudDetectedConfirmedEncour() : Observable<any> {
    return this.http.get(this.BASE_URL + "frauddetectdconfrmedencour/", 
    {headers : this.HTTP_HEADERS})
  }

  fraudBillingCat() : Observable<any> {
    return this.http.get(this.BASE_URL + "fraudbillingcat/", 
    {headers : this.HTTP_HEADERS})
  }

  fraudSubStatus() : Observable<any> {
    return this.http.get(this.BASE_URL + "fraudsubstatus/", 
    {headers : this.HTTP_HEADERS})
  }

  fraudLastDateParRegion() : Observable<any> {
    return this.http.get(this.BASE_URL + "fraudlastdateparregion/", 
    {headers : this.HTTP_HEADERS})
  }

// Second Page
  fraudAnalyseDates() : Observable<any> {
    return this.http.get(this.BASE_URL + "fraudanalysedates/", 
    {headers : this.HTTP_HEADERS})
  }


  downloadExcelFile(date: string): Observable<any> {
    return this.http.get(this.BASE_URL + "downloadcsv/", 
    {
      params: { date },
      headers : new HttpHeaders({'Content-Type' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                'Content-Disposition': 'attachment; filename="data.xlsx"'}),
      responseType: 'blob',
    });
  }
}
