import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RouterModule } from "@angular/router";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { CardModule } from './card/card.module';

import { FooterComponent } from "./footer/footer.component";
import { NavbarComponent } from "./navbar/navbar.component";
import { SidebarComponent } from "./sidebar/sidebar.component";
import { Card2Component } from './card2/card2.component';

@NgModule({
  imports: [CommonModule, RouterModule, NgbModule, CardModule],
  declarations: [FooterComponent, NavbarComponent, SidebarComponent, Card2Component],
  exports: [FooterComponent, NavbarComponent, SidebarComponent, CardModule, Card2Component]
})
export class ComponentsModule {}
