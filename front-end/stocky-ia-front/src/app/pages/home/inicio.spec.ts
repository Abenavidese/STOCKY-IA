import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InicioTs } from './inicio.js';

describe('InicioTs', () => {
  let component: InicioTs;
  let fixture: ComponentFixture<InicioTs>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InicioTs]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InicioTs);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
