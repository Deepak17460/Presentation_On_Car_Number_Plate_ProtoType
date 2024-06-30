import { Component, OnInit, ViewChild } from '@angular/core';
import { FileUploadService } from 'src/app/services/fileUploadService/file-upload.service';
import Swal from 'sweetalert2';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { HttpClient, HttpHeaders } from '@angular/common/http';

export interface TableData {
  sno: number;
  vehicleNumber: string;
  entryTime: string;
}


@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent implements OnInit {
  defaultFileName = 'example.mp4';
  defaultFileType = 'video/mp4';
  uploadProgress: number = 0;
  selectedFileName: string | null = null;
  dataSource = new MatTableDataSource<TableData>([]);
  displayedColumns: string[] = ['sno', 'vehicleNumber', 'entryTime'];
  private apiUrl = 'http://127.0.0.1:5000/'; 
  @ViewChild(MatPaginator, { static: true }) paginator!: MatPaginator;

  file: File = new File(['Hello.mp4'], this.defaultFileName, { type: this.defaultFileType });
  
  constructor(private fileUploadService: FileUploadService,private http: HttpClient) {}

  onFileSelected(event: any): void {
    console.log(event);
    this.file = event.target.files[0];
    if (this.file) {
      this.selectedFileName = this.file.name; 
      Swal.fire({
        title: 'Uploading...',
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        didOpen: () => {
          Swal.showLoading();
        }
      });
      
      this.fileUploadService.uploadFile(this.file).subscribe(
        progress => {
          
          this.uploadProgress = progress;
          if (progress === 100) {
            Swal.close(); 
            Swal.fire({
              icon: 'success',
              title: 'File Uploaded Successfully!',
              showConfirmButton: false,
              timer: 1500
            });
          }
        },
        error => {
          Swal.close(); 
          Swal.fire({
            icon: 'error',
            title: 'Upload Failed',
            text: 'There was an error while uploading the file. Please try again later.'
          });
        }
      );
    }
  }

  ngOnInit(): void {
    let i = 1;
    const headers = new HttpHeaders().set('Content-Type', 'application/json');

    this.http.get(`${this.apiUrl}get_data`, {
      headers: headers
    }).subscribe((result: any) => {
      
      this.dataSource.data = result.map((item:any) => { return { carNo: item[1], timestamp: item[2] }});
      console.log(this.dataSource.data);
      this.dataSource.paginator = this.paginator;
    })
    
  }

  processing(): void {
    if(this.file){
    console.log(this.file);
    this.fileUploadService.Processing(this.file).subscribe(res=>{
      console.log("Normal");
    });
    }
}

 OptimalProcessing(): void {
        if(this.file){
            console.log("optimal");
        console.log(this.file);
        this.fileUploadService.OptimalProcessing(this.file).subscribe(res=>{
          console.log("Completed");
        });
        }
    }



}
