double phase = 0;

void calculate(){
    double step = frequency/SAMPLERATE;
    phase += step;
    if(phase >= 1)
        phase -= 1;
    if(phase < 0)
        phase += 1;
    output = sin(phase * 2 * PI);
}