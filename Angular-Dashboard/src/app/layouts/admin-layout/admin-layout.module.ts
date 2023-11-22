import { NgModule } from "@angular/core";
import { HttpClientModule } from "@angular/common/http";
import { RouterModule } from "@angular/router";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ComponentsModule } from "../../components/components.module";
import { AdminLayoutRoutes } from "./admin-layout.routing";
import { DashboardComponent } from "../../pages/dashboard/dashboard.component";
import { DownloadsComponent } from "../../pages/downloads/downloads.component";

import { NgbModule } from "@ng-bootstrap/ng-bootstrap";

import * as PlotlyJS from 'plotly.js/dist/plotly.js';
import { PlotlyModule } from 'angular-plotly.js';
PlotlyModule.plotlyjs = PlotlyJS;


@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(AdminLayoutRoutes),
    FormsModule,
    PlotlyModule,
    HttpClientModule,
    NgbModule,
    ComponentsModule
  ],
  declarations: [
    DashboardComponent,
    DownloadsComponent,
  ],
})
export class AdminLayoutModule {}
