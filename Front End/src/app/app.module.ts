import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app.routing';
import { ComponentsModule } from './components/components.module';

import { AppComponent } from './app.component';
import { CommonModule } from '@angular/common';
import { IgxPieChartModule } from 'igniteui-angular-charts';

import { DashboardComponent } from './dashboard/dashboard.component';
import { RegressionComponent } from './regression/regression.component';
import { BinaryclassificationComponent } from './binaryclassification/binaryclassification.component';
import { MulticlassificationComponent } from './multiclassification/multiclassification.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { TableListComponent } from './table-list/table-list.component';
import { TypographyComponent } from './typography/typography.component';
import { IconsComponent } from './icons/icons.component';
import { MapsComponent } from './maps/maps.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { UpgradeComponent } from './upgrade/upgrade.component';
import {
  AgmCoreModule
} from '@agm/core';
import { AdminLayoutComponent } from './layouts/admin-layout/admin-layout.component';



@NgModule({
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    ComponentsModule,
    RouterModule,
    AppRoutingModule,
    CommonModule,
    IgxPieChartModule,
    AgmCoreModule.forRoot({
      apiKey: 'YOUR_GOOGLE_MAPS_API_KEY'
    })
  ],
  declarations: [
    AppComponent,
    AdminLayoutComponent,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
