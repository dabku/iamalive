import { Component, OnDestroy, OnInit } from '@angular/core';

import { ConnectionstateService, IPongMessage } from '../services/connectionstate.service';

@Component({
  selector: 'app-connectionstate',
  templateUrl: './connectionstate.component.html',
  styleUrls: ['./connectionstate.component.css']
})





export class ConnectionstateComponent implements OnInit, OnDestroy {
  public message: State;
  State = State;
  constructor(public connectionstateService: ConnectionstateService) { }
  private interval;

  ngOnInit() {
    this.getConnectionState();
    this.interval = setInterval(() => {
    this.getConnectionState();
  }, 5000);
  }

  ngOnDestroy() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  }

  getConnectionState(): void {
    this.connectionstateService.getConnectionState().subscribe(data => this.postprocess(data));
  }


  postprocess(new_data: IPongMessage): void
  {
     if (new_data.message === 'pong')
    {
      this.message = State.OK;
    } else {
      this.message = State.ERROR;
    }

  }

}

export enum State{
  OK = 'Connection OK',
  ERROR = 'Connection Failed'
}