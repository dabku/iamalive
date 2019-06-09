import { TestBed } from '@angular/core/testing';

import { ConnectionstateService } from './connectionstate.service';

describe('ConnectionstateService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ConnectionstateService = TestBed.get(ConnectionstateService);
    expect(service).toBeTruthy();
  });
});
