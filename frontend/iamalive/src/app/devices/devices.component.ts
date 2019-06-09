import { Component, OnInit, OnDestroy } from '@angular/core';
import { DeviceService } from '../services/device.service';
import { Device } from '../device.model';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.css']
})
export class DevicesComponent implements OnInit, OnDestroy {

  public devices: Device[];
  private interval;
  selectedDevice: Device;


  constructor(public deviceService: DeviceService) { }

  ngOnInit() {
    this.getDevices();
    this.interval = setInterval(() => {
      this.getDevices();
    }, 5000);
  }
  ngOnDestroy() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  }
  getDevices(): void {
    this.deviceService.getDevices().subscribe(data => {
      this.devices = data;
      if (this.selectedDevice) {
        this.selectedDevice = this.devices.find(x => x.name === this.selectedDevice.name);
      } else if (this.devices) {
        this.selectedDevice = this.devices[0];
      }
    });
  }
  onSelect(device: Device): void {
    this.selectedDevice = device;
  }
  doSomething(event) {
    console.log(event);
  }

}
