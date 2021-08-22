#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
const int N = 5;
const double size = 100;
const double dt = 0.001;
const double tim = 10;
const double v = 10;
const double eps = 200;
const double sigma = 10;


struct molecule{
	double x;
	double y;
	double z;
	double x_real;
	double y_real;
	double z_real;
	double x_p;
	double y_p;
	double z_p;
};

void calc_molecule(molecule* input, int n, double* output){
	double x, y, z, k, force, r;
	output[0] = 0;
	output[1] = 0;
	output[2] = 0;
	output[3] = 0;
	for (int i = 0; i<N*N*N; i++){
		if (i == n){
			continue;
		}
		for (int l = -1; l < 2; l++){
			for (int j = -1; j < 2; j++){
				for (int m = -1; m<2; m++){
					x = input[i].x + l*size;
					y = input[i].y + j*size;
					z = input[i].z + m*size;
					r = sqrt(pow((input[n].x - x), 2) + pow((input[n].y -y), 2) + pow((input[n].z - z), 2));
					k = pow(sigma, 6)/pow(r, 6)*4;
					output[0] = output[0] + k*k/8*eps - k*eps/2;
					force = -3*k*k/r*eps + 6*k/r*eps;
					output[1] = output[1] + force * (x - input[n].x)/r;
					output[2] = output[2] + force * (y - input[n].y)/r;
					output[3] = output[3] + force * (z - input[n].z)/r;
				}
			}
		}
	}
}

int main(){
	double t = 0;
	double r, force;
	double acceleration_x, acceleration_y, acceleration_z, energy, k, kin, imp_x, imp_y, imp_z;
	double i_x, i_y, i_z, sp;
	std::random_device rd;
	std::default_random_engine coords(rd());
	std::uniform_int_distribution<> uniform_dist(0, size);
	std::normal_distribution<> normal_dist(0.0, v*dt);
	molecule molecules[N*N*N];
	molecule temp[N*N*N];
	std::ofstream output, en_output, kin_en, impulses, speeds, real_coords, speed_pr;
	output.open("output.txt");
	speed_pr.open("speed_prods.txt");
	speeds.open("speeds.txt");
	en_output.open("energy.txt");
	kin_en.open("kin_en.txt");
	impulses.open("impulses.txt");
	real_coords.open("real_output.txt");
	output << N*N*N << ' ' << dt << ' ';
	double out[4];
	for (int i=0; i<N; i++){
		for (int j=0; j<N; j++){
			for (int k=0; k<N; k++){
				molecules[N*N*i + N*j + k].x = size/N*(k+0.5);
				molecules[N*N*i + N*j + k].y = size/N*(i+0.5);
				molecules[N*N*i + N*j + k].z = size/N*(j+0.5);
			}
		}
	}
	for (int i=0; i<N*N*N; i++){
		molecules[i].x_p = molecules[i].x + normal_dist(coords);
		molecules[i].y_p = molecules[i].y + normal_dist(coords);
		molecules[i].z_p = molecules[i].z + normal_dist(coords);
	}
	while (t < tim){ 
		energy = 0;
		std::cout << t << std::endl;
		kin = 0;
		imp_x = 0;
		imp_y = 0;
		imp_z = 0;
		for (int i=0; i<N*N*N; i++){
			calc_molecule(molecules, i, out);
			energy = energy + out[0];
			acceleration_x = out[1];
			acceleration_y = out[2];
			acceleration_z = out[3];
			i_x = (molecules[i].x - molecules[i].x_p)/dt;
			i_y = (molecules[i].y - molecules[i].y_p)/dt;
			i_z = (molecules[i].z - molecules[i].z_p)/dt;
			imp_x += i_x;
			imp_y += i_y;
			imp_z += i_z;
			speed_pr << i_x << " " << i_y << " " << i_z << " ";
			sp = (i_x*i_x + i_y*i_y + i_z*i_z)/2;
			kin += sp;
			speeds << sqrt(2*sp) << ' ';
			temp[i].x = 2*molecules[i].x - molecules[i].x_p + acceleration_x *dt*dt;
			temp[i].y = 2*molecules[i].y - molecules[i].y_p + acceleration_y *dt*dt;
			temp[i].z = 2*molecules[i].z - molecules[i].z_p + acceleration_z *dt*dt;
			temp[i].x_p = molecules[i].x;
			temp[i].y_p = molecules[i].y;
			temp[i].z_p = molecules[i].z;
			molecules[i].x_real = molecules[i].x_real + molecules[i].x - molecules[i].x_p + acceleration_x * dt*dt;
			molecules[i].y_real = molecules[i].y_real + molecules[i].y - molecules[i].y_p + acceleration_y * dt * dt;
			molecules[i].z_real = molecules[i].z_real + molecules[i].z - molecules[i].z_p + acceleration_z * dt * dt;
			if (temp[i].x > size){
				temp[i].x = temp[i].x - size;
				temp[i].x_p = temp[i].x_p - size;
			}
			if (temp[i].x < 0.0){
				temp[i].x = temp[i].x + size;
				temp[i].x_p = temp[i].x_p + size;
			}
			if (temp[i].y > size){
				temp[i].y = temp[i].y - size;
				temp[i].y_p = temp[i].y_p - size;
			}
			if (temp[i].y < 0.0){
				temp[i].y = temp[i].y + size;
				temp[i].y_p = temp[i].y_p + size;
			}
			if (temp[i].z > size){
				temp[i].z = temp[i].z - size;
				temp[i].z_p = temp[i].z_p - size;
			}
			if (temp[i].z < 0.0){
				temp[i].z = temp[i].z + size;
				temp[i].z_p = temp[i].z_p + size;
			}
		}
		for (int i=0; i<N*N*N; i++){
			molecules[i].x_p = temp[i].x_p;
			molecules[i].x = temp[i].x;
			molecules[i].y_p = temp[i].y_p;
			molecules[i].y = temp[i].y;
			molecules[i].z_p = temp[i].z_p;
			molecules[i].z = temp[i].z;
		}
		for (int i=0; i<N*N*N; i++){
			output << molecules[i].x << ' ' << molecules[i].y << ' ' << molecules[i].z << ' ';
			real_coords << molecules[i].x_real << ' ' << molecules[i].y_real << ' ' << molecules[i].z_real << ' ';
		}
		en_output << energy << ' ';
		kin_en << kin << ' ';
		impulses << imp_x << ' ' << imp_y << ' ' << imp_z << ' ';
		t = t + dt;
	}
	return 0;
}
