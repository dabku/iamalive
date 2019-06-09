import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ConnectionstateComponent } from './connectionstate.component';

describe('ConnectionstateComponent', () => {
  let component: ConnectionstateComponent;
  let fixture: ComponentFixture<ConnectionstateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ConnectionstateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConnectionstateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
