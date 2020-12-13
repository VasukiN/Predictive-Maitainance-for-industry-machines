import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MulticlassificationComponent } from './multiclassification.component';

describe('MulticlassificationComponent', () => {
  let component: MulticlassificationComponent;
  let fixture: ComponentFixture<MulticlassificationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MulticlassificationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MulticlassificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
