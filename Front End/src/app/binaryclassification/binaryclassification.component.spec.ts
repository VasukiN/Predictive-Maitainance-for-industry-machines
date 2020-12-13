import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BinaryclassificationComponent } from './binaryclassification.component';

describe('BinaryclassificationComponent', () => {
  let component: BinaryclassificationComponent;
  let fixture: ComponentFixture<BinaryclassificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BinaryclassificationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BinaryclassificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
