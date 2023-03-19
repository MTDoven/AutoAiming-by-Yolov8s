#include<windows.h>
#include<math.h>
#define MAX_ITEMS 8
#define CONFIGENCE_BOUND 0.6

typedef struct {
    float confidence;
    float size;
    float distence;
    float x1;
    float y1;
    float x2;
    float y2;
} Person;

extern "C" __declspec(dllexport)
void MouseMove(int dx,int dy) {
    mouse_event(MOUSEEVENTF_MOVE,dx,dy,0,0);
}
void ProcessForce(float* x, float* y){
    (*x) = (*x)/20;
    (*y) = (*y)/20;
    if ((*x)<2 && (*x)>0.2) (*x)=2;
    else if((*x)>-10 && (*x)<-0.2) (*x)=-10;
    if ((*y)<2 && (*y)>0.2) (*y)=2;
    else if((*y)>-2 && (*y)<-0.2) (*y)=-2;
}
bool is_covering_the_line(Person obj){
    if(!(obj.x1<320 && obj.x2>320)) return false;
    if(obj.y1<320 && obj.y2>320) return true;
    if(obj.y1<480 && obj.y2>480) return true;
    if(obj.y1>320 && obj.y2<480) return true;
    return false;
}



extern "C" __declspec(dllexport)
void callback(float array[MAX_ITEMS][6]){
    Person persons[MAX_ITEMS]={0};
    Person the_vary_person;
    int items_count=0;

    for(int i=0; i<MAX_ITEMS; i++){
        if(array[i][5]>0.999) continue;
        if(array[i][4]<CONFIGENCE_BOUND) break;
        persons[items_count].confidence = array[i][4];
        persons[items_count].x1 = array[i][0];
        persons[items_count].y1 = array[i][1];
        persons[items_count].x2 = array[i][2];
        persons[items_count].y2 = array[i][3];
        persons[items_count].size = (array[i][2]-array[i][0])*(array[i][3]-array[i][1]);
        persons[items_count].distence = fabs((array[i][0]+array[i][2])/2-320)+fabs((array[i][1]+array[i][3])/2-320);
        items_count++;
    } // get information
    if(items_count==0) return;

    for(int i=0; i<items_count; i++)
        for(int j=0; j<items_count-i-1; j++)
            if(persons[j].distence>persons[j+1].distence){
                Person temp = persons[j];
                persons[j] = persons[j+1];
                persons[j+1] = temp; }
    for(int i=0; i<items_count; i++){
        if(is_covering_the_line(persons[i])){
            the_vary_person = persons[i];
            goto ChooseFinished; }
    } // Choose the one had been aimed.

    for(int i=0; i<items_count; i++)
        for(int j=0; j<items_count-i-1; j++)
            if(persons[j].size<persons[j+1].size){
                Person temp = persons[j];
                persons[j] = persons[j+1];
                persons[j+1] = temp; }
    if(persons[0].size > persons[1].size*4){
        the_vary_person = persons[0];
        goto ChooseFinished;
    } // Choose the biggest one

    for(int i=0; i<items_count; i++)
        for(int j=0; j<items_count-i-1; j++)
            if(persons[j].distence>persons[j+1].distence){
                Person temp = persons[j];
                persons[j] = persons[j+1];
                persons[j+1] = temp; }
    the_vary_person = persons[0];
    goto ChooseFinished;
    // Choose the nearest one

    ChooseFinished:
    float x_direct = (the_vary_person.x1+the_vary_person.x2)/2-320;
    float y_direct = (the_vary_person.y1+the_vary_person.y2)/2-320;
    ProcessForce(&x_direct, &y_direct);
    MouseMove(round(x_direct), round(y_direct));

}

