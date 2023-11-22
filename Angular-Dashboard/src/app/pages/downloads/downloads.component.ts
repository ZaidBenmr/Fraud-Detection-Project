import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../api.service';
import * as XLSX from 'xlsx';


@Component({
  selector: 'app-downloads',
  templateUrl: './downloads.component.html',
  styleUrls: ["./downloads.component.scss"],  
  providers : [ApiService]
})
export class DownloadsComponent implements OnInit {

  fraud_analyse_dates : any
  blob                : any
  selectedDate        : string;
  excelData           : any[] = [];
  tableColumns        : string[] = [
                      'DELIVERY_POINT_ID',
                      'NUM_CTA_ABT_EA',
                      'NUM_CTA_ABT_BT',
                      'CONSUMER_BILLING_ID',
                      'DELIVERY_POINT_ADDRESS',
                      'SUBSCRIPTION_STATUS_LBL',
                      'BILLING_CATEGORY_ELEC',
                      'METIER',
                      'PROBABILITE',
                      'REGION',
                      'DATE_ANALYSE',
                      'CONFIRMATION'
                    ];
   public condition : boolean = false


  constructor(private api : ApiService) { 
    this.fraudAnalyseDates();
  }

  importFile(): void {
    this.api.downloadExcelFile(this.selectedDate).subscribe((blob: Blob) => {
      this.blob = blob
      this.displayFile()
    });
    
  }

  downloadFile(): void {
    if (this.blob) {
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(this.blob);
      link.download = 'MyFile.xlsx';  // Replace with the desired file name
      link.click();
    } else {
      // Handle the case when no file has been imported yet
      console.log('No file has been imported yet');
    }

  }

  displayFile(): void {
    const fileReader = new FileReader();
    fileReader.onload = (e) => {
      const data = new Uint8Array(fileReader.result as ArrayBuffer);
      const workbook = XLSX.read(data, { type: 'array' });
      const worksheet = workbook.Sheets[workbook.SheetNames[0]];
      const sheetData = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });
  
      this.excelData = sheetData.slice(1).map(row => {
        const rowData: any = {};
        for (let i = 0; i < this.tableColumns.length; i++) {
          let value = row[i];
          // Check if the column is 'DATE_ANALYSE'
          if (this.tableColumns[i] === 'DATE_ANALYSE') {
            // Convert the numeric value to a date string
            const dateValue = XLSX.SSF.format('yyyy-mm-dd', Number(value));
            value = dateValue || ''; // Set empty string if format conversion fails
          }
          rowData[this.tableColumns[i]] = value;
        }
        return rowData;
      });
  
      this.condition = true;
    };
  
    fileReader.readAsArrayBuffer(this.blob);
  }
  
  

  fraudAnalyseDates = () => {
    this.api.fraudAnalyseDates().subscribe(
      data => {
        this.fraud_analyse_dates = data
        console.log(data)
      },
      error => {
        console.log(error)
      }
    )
  }


  ngOnInit() {
  }

}
