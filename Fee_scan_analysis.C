#include <iostream>
#include <fstream>
#include <vector>
#include <TGraph.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TF1.h>
#include <TH1.h>
#include <TH2.h>
#include "TFile.h"

using namespace std;

class scan {
   public:
   	    string tdc;
        int card;
        int asic;
        int channel;
        int width;
        int peak;
        int status;  
   	    string file_name;

};


bool Fee_scan_analysis()
{

    TFile* scan_results = new TFile("BS_D_G1.root", "RECREATE");


    ifstream iFile("BS_D_G1.txt");  

    scan sc_obj;
    vector<scan> vec_data;  

    while (!iFile.eof())
    {
        string tdc;
        int card;
        int asic;
        int channel;
        int width;
        int peak;
        int status;
   	    string file_name;

        iFile >> tdc >>card >> asic >> channel >> width >> peak >> status >> file_name;

        sc_obj.tdc = tdc;
        sc_obj.card = card;
        sc_obj.asic = asic;
        sc_obj.channel = channel;
        sc_obj.width = width;
        sc_obj.peak = peak;
        sc_obj.status = status;
        sc_obj.file_name = file_name;

        vec_data.push_back(sc_obj);
        //cout<<"SIZE : "<<"\t"<<tdc<<"\t"<<card<<"\t"<<asic<<"\t"<<channel<<"\t"<<width<<"\t"<<peak<<"\t"<<status<<"\t"<<file_name<<endl;


    }

    TH2F* h0 = new TH2F("h0","Case 0;Baseline;Width [mV]",34,-1,33,34,-1,33);
    TH2F* h1 = new TH2F("h1","Case 1;Baseline;Width [mV]",34,-1,33,34,-1,33);
    TH2F* h2 = new TH2F("h2","Case 2;Baseline;Width [mV]",34,-1,33,34,-1,33);
    TH2F* h3 = new TH2F("h3","Case 3;Baseline;Width [mV]",34,-1,33,34,-1,33);
    TH2F* h4 = new TH2F("h4","Case 4;Baseline;Width [mV]",35,-1,34,35,-1,34);
    TH1F* h_count = new TH1F("h_count","Baseline_scan;Cases",5,0,5);
    TH1F* h1_width = new TH1F("h1_width","Baseline_scan;Baseline_width [mV]",33,-1,32);
    TH1F* h1_peak = new TH1F("h1_peak","Baseline_scan;Baseline_position [mV]",32,0,32);
    // TH1F* h1_width = new TH1F("h1_width","Threshold_scan;Baseline_width [LSB]",33,-1,32);
    // TH1F* h1_peak = new TH1F("h1_peak","Threshold_scan;Baseline_position [LSB]",32,0,32);

for ( int i =0; i <vec_data.size()-1; i++)
{
	if (vec_data[i].status==0)
	{
			h0->Fill(vec_data[i].peak,vec_data[i].width);
			h_count->Fill(0);
			h1_width->Fill(vec_data[i].width);
			h1_peak->Fill(vec_data[i].peak);

	}
	else if (vec_data[i].status==1)
	{
			h1->Fill(vec_data[i].peak,vec_data[i].width);
			h_count->Fill(1);
			h1_width->Fill(vec_data[i].width);
			h1_peak->Fill(vec_data[i].peak);


	}
	else if (vec_data[i].status==2)
	{
			h2->Fill(vec_data[i].peak,vec_data[i].width);
			h_count->Fill(2);
			h1_width->Fill(vec_data[i].width);
			h1_peak->Fill(vec_data[i].peak);


	}
	else if (vec_data[i].status==3)
	{
			h3->Fill(vec_data[i].peak,vec_data[i].width);
			h_count->Fill(3);
			h1_width->Fill(vec_data[i].width);
			h1_peak->Fill(vec_data[i].peak);


	}
	else if (vec_data[i].status==4)
	{
			h4->Fill(vec_data[i].peak,vec_data[i].width);
			h_count->Fill(4);
			h1_width->Fill(vec_data[i].width);
			h1_peak->Fill(vec_data[i].peak);


	}

}
	h_count->GetXaxis()->SetBit(TAxis::kLabelsHori);
   	h_count->GetXaxis()->SetBinLabel(1,"Case 0");
   	h_count->GetXaxis()->SetBinLabel(2,"Case 1");
	h_count->GetXaxis()->SetBinLabel(3,"Case 2");
   	h_count->GetXaxis()->SetBinLabel(4,"Case 3");
   	h_count->GetXaxis()->SetBinLabel(5,"Case 4");

    h1_width->GetXaxis()->SetTitle("Baseline width [LSB]");
    h1_width->GetYaxis()->SetTitle("Counts");

	//hx->Draw();
	h0->Write();
	h1->Write();
	h2->Write();
	h3->Write();
	h4->Write();
	h_count->Write();
	h1_width->Write();
	h1_peak->Write();

	return 0;
}
