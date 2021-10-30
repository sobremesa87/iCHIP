v {xschem version=2.9.9 file_version=1.2 

* Copyright 2020 Stefan Frederik Schippers
* 
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.

}
G {}
K {}
V {}
S {}
E {}
N 440 -240 460 -240 {lab=B}
N 380 -240 400 -240 {lab=G1v8}
N 440 -290 440 -270 {lab=#net1}
N 440 -210 440 -190 {lab=S}
N 690 -240 710 -240 {lab=B}
N 630 -240 650 -240 {lab=G1v8}
N 690 -290 690 -270 {lab=#net2}
N 690 -210 690 -190 {lab=S}
N 440 -370 440 -350 { lab=D1v8}
N 690 -370 690 -350 { lab=D1v8}
N 390 -370 1370 -370 { lab=D1v8}
N 940 -240 960 -240 {lab=B}
N 940 -290 940 -270 {lab=#net3}
N 940 -210 940 -190 {lab=S}
N 1190 -240 1210 -240 {lab=B}
N 1130 -240 1150 -240 {lab=G1v8}
N 1190 -290 1190 -270 {lab=#net4}
N 1190 -210 1190 -190 {lab=S}
N 940 -370 940 -350 { lab=D1v8}
N 1190 -370 1190 -350 { lab=D1v8}
N 880 -240 900 -240 {lab=G1v8}
N 440 -530 440 -480 { lab=GND}
N 440 -620 440 -590 { lab=vds}
N 360 -580 400 -580 { lab=D1v8}
N 360 -540 400 -540 { lab=S}
N 360 -620 440 -620 { lab=vds}
C {devices/code.sym} 50 -190 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval( @value )"
value="
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_01v8/sky130_fd_pr__nfet_01v8__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_01v8_lvt/sky130_fd_pr__nfet_01v8_lvt__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_01v8/sky130_fd_pr__pfet_01v8__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_03v3_nvt/sky130_fd_pr__nfet_03v3_nvt__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_05v0_nvt/sky130_fd_pr__nfet_05v0_nvt__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/esd_nfet_01v8/sky130_fd_pr__esd_nfet_01v8__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_01v8_lvt/sky130_fd_pr__pfet_01v8_lvt__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_01v8_hvt/sky130_fd_pr__pfet_01v8_hvt__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/esd_pfet_g5v0d10v5/sky130_fd_pr__esd_pfet_g5v0d10v5__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_g5v0d10v5/sky130_fd_pr__pfet_g5v0d10v5__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_g5v0d16v0/sky130_fd_pr__pfet_g5v0d16v0__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_g5v0d10v5/sky130_fd_pr__nfet_g5v0d10v5__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_g5v0d16v0/sky130_fd_pr__nfet_g5v0d16v0__tt_discrete.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/esd_nfet_g5v0d10v5/sky130_fd_pr__esd_nfet_g5v0d10v5__tt.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/models/corners/tt/nonfet.spice
* Mismatch parameters
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_01v8/sky130_fd_pr__nfet_01v8__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_01v8/sky130_fd_pr__pfet_01v8__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_01v8_lvt/sky130_fd_pr__nfet_01v8_lvt__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_01v8_lvt/sky130_fd_pr__pfet_01v8_lvt__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_01v8_hvt/sky130_fd_pr__pfet_01v8_hvt__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_g5v0d10v5/sky130_fd_pr__nfet_g5v0d10v5__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/pfet_g5v0d10v5/sky130_fd_pr__pfet_g5v0d10v5__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_05v0_nvt/sky130_fd_pr__nfet_05v0_nvt__mismatch.corner.spice
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_03v3_nvt/sky130_fd_pr__nfet_03v3_nvt__mismatch.corner.spice
* Resistor\\\\$::SKYWATER_MODELS\\\\/Capacitor
.include \\\\$::SKYWATER_MODELS\\\\/models/r+c/res_typical__cap_typical.spice
.include \\\\$::SKYWATER_MODELS\\\\/models/r+c/res_typical__cap_typical__lin.spice
* Special cells
.include \\\\$::SKYWATER_MODELS\\\\/models/corners/tt/specialized_cells.spice
* All models
.include \\\\$::SKYWATER_MODELS\\\\/models/all.spice
* Corner
.include \\\\$::SKYWATER_MODELS\\\\/models/corners/tt/rf.spice
"}
C {devices/title.sym} 160 -30 0 0 {name=l1 author="sobremesa87"}
C {devices/lab_pin.sym} 390 -370 0 0 {name=p17 lab=D1v8}
C {devices/lab_pin.sym} 440 -190 0 1 {name=p3 lab=S}
C {devices/lab_pin.sym} 460 -240 0 1 {name=p4 lab=B}
C {devices/ammeter.sym} 440 -320 0 0 {name=Vn_lvt_long current=5.7132e-04}
C {devices/lab_pin.sym} 690 -190 0 1 {name=p11 lab=S}
C {devices/lab_pin.sym} 710 -240 0 1 {name=p21 lab=B}
C {devices/ammeter.sym} 690 -320 0 0 {name=Vn_long current=5.0094e-04}
C {devices/lab_pin.sym} 380 -240 0 0 {name=p2 lab=G1v8}
C {devices/lab_pin.sym} 630 -240 0 0 {name=p6 lab=G1v8}
C {devices/ipin.sym} 270 -520 0 0 {name=p48 lab=G1v8}
C {devices/ipin.sym} 270 -480 0 0 {name=p49 lab=D1v8}
C {devices/ipin.sym} 270 -440 0 0 {name=p50 lab=B}
C {devices/code_shown.sym} 0 -940 0 0 {name=NGSPICE
only_toplevel=true
value="* this experimental option enables mos model bin 
* selection based on W/NF instead of W
.option wnflag=1 
.option savecurrents
vg G1v8 0 1.8
vs s 0 0
vd D1v8 0 1.8
vb b 0 0
.control
set filetype=ascii
save all
dc vd 0 1.8 0.01 
*plot all.Vn_long#branch vs vds
write skywater_char_NMOS_vds.raw
.endc
" }
C {devices/ngspice_get_value.sym} 450 -270 0 0 {name=r1 node="i(@m.xm1.msky130_fd_pr__nfet_01v8_lvt[id])"
descr="Id="}
C {devices/ngspice_get_value.sym} 370 -270 0 0 {name=r2 node=@m.xm1.msky130_fd_pr__nfet_01v8_lvt[gm]
descr="gm="}
C {devices/code.sym} 50 -340 0 0 {name=nfet_20v0_MODEL
only_toplevel=true
format="tcleval( @value )"
value="
.include \\\\$::SKYWATER_MODELS\\\\/cells/nfet_20v0/sky130_fd_pr__nfet_20v0__tt_discrete.corner.spice
"}
C {devices/lab_pin.sym} 940 -190 0 1 {name=p12 lab=S}
C {devices/lab_pin.sym} 960 -240 0 1 {name=p5 lab=B}
C {devices/ammeter.sym} 940 -320 0 0 {name=Vn_lvt_short current=5.7132e-04}
C {devices/lab_pin.sym} 1190 -190 0 1 {name=p13 lab=S
}
C {devices/lab_pin.sym} 1210 -240 0 1 {name=p8 lab=B}
C {devices/ammeter.sym} 1190 -320 0 0 {name=Vn_short current=5.0094e-04}
C {devices/lab_pin.sym} 1130 -240 0 0 {name=p9 lab=G1v8}
C {devices/ngspice_get_value.sym} 950 -270 0 0 {name=r3 node="i(@m.xm1.msky130_fd_pr__nfet_01v8_lvt[id])"
descr="Id="}
C {devices/lab_pin.sym} 880 -240 0 0 {name=p10 lab=G1v8}
C {devices/lab_pin.sym} 360 -580 0 0 {name=l3 sig_type=std_logic lab=D1v8}
C {devices/lab_pin.sym} 360 -540 0 0 {name=l4 sig_type=std_logic lab=S}
C {devices/gnd.sym} 440 -480 0 0 {name=l5 lab=GND}
C {sky130_fd_pr/nfet_01v8.sym} 670 -240 0 0 {name=M1
L=2
W=10
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 420 -240 0 0 {name=M2
L=2
W=10
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8.sym} 1170 -240 0 0 {name=M3
L=0.15
W=10
nf=1 
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet_01v8_lvt.sym} 920 -240 0 0 {name=M4
L=0.15
W=10
nf=1
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'" 
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'" 
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8_lvt
spiceprefix=X
}
C {devices/lab_wire.sym} 360 -620 0 0 {name=l2 sig_type=std_logic lab=vds}
C {devices/vcvs.sym} 440 -560 0 0 {name=E1 value=1}
