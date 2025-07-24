import { TestBed } from '@angular/core/testing';

import { Predictions } from './predictions';

describe('Predictions', () => {
  let service: Predictions;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Predictions);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
