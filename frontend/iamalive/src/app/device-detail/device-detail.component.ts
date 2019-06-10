import { Component, OnInit, Input } from '@angular/core';
import {Device} from '../device.model';


@Component({
  selector: 'app-device-detail',
  templateUrl: './device-detail.component.html',
  styleUrls: ['./device-detail.component.css']
})
export class DeviceDetailComponent implements OnInit {

  @Input()  device: Device;

  constructor() { }

  ngOnInit() {
  }
  switchEditMode(){
    alert('Not implemented');
  }
}
