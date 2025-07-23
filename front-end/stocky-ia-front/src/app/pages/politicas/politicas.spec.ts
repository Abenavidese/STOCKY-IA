import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Politicas } from './politicas';

describe('Politicas', () => {
  let component: Politicas;
  let fixture: ComponentFixture<Politicas>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Politicas]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Politicas);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
