import { NgModule } from '@angular/core';
import { RouterModule,Routes } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HomepageComponent } from './components/homepage/homepage.component';







const routes: Routes = [
  { 
    path: "" , component: HomepageComponent
  },
  
];


@NgModule({
  declarations: [],
  imports: [RouterModule.forRoot(routes)],
    exports:[RouterModule]
  
})
export class AppRoutingModule { }





 