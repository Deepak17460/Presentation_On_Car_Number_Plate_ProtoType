import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { delay } from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';
@Injectable({
  providedIn: 'root'
}) 
export class FileUploadService {
  
  private apiUrl = 'http://127.0.0.1:5000/'; 

  constructor(private http:HttpClient) {}

  uploadFile(file: File): Observable<number> {
    
    return of(100).pipe(delay(1500));
  }

  Processing(file:File):Observable<any>{
      const formData:FormData=new FormData();
      formData.append("video",file,file.name);

      console.log(formData);
      return this.http.post(this.apiUrl+'video',formData);
  }
  OptimalProcessing(file:File):Observable<any>{
    const formData:FormData=new FormData();
    formData.append("video",file,file.name);

    console.log(formData);
    return this.http.post(this.apiUrl+'optimal',formData);
}
}
