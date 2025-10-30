% Constants
t       = 120;
dt      = simu.dt;                                  % 0.002 s
tstep   = t/dt + 1;                                 % Timestep index
A       = AOE.Unit1.Cylinder.CrossSectionalArea;    % Cylinder cross-sectional area = 4.4380 m2

% Pressure forces
Pu          = P_C2(tstep, 2);   % Upper chamber pressure
Pl          = P_C1(tstep, 2);   % Lower chamber pressure
F_pu        = Pu * A;           % Upper chamber pressure force
F_pl        = Pl * A;           % Lower chamber pressure force
Fp          = F_PTO(tstep, 2);  % Total pressure force
Fp_check    = F_pu - F_pl;      % Total pressure force check

% PTO reaction force
Fc          = F_Friction(tstep, 2);             % Friction force
Fstop_hi    = Fstop_High(tstep, 2);             % High endstop force
Fstop_lo    = Fstop_Low(tstep, 2);              % Low endstop force
Fpto        = F_T(tstep, 2);                    % PTO force
Fpto_check  = Fp + Fc + Fstop_hi + Fstop_lo;    % PTO force check
Fpto_ws     = output.ptos.forceTotal(:,3);



% Hydrodynamic force
F_float     = output.bodies(1).forceTotal(:,3);
F_f         = F_float(tstep);                   % Float
F_spar      = output.bodies(2).forceTotal(:,3);
F_s         = F_spar(tstep);                    % Spar
F_relative  = F_float - F_spar;
F_rel       = F_f - F_s;


close all
hold on
plot(linspace(0,simu.time(end), length(F_T(:,2))), F_T(:,2))
plot(linspace(0,simu.time(end), length(F_T(:,2))), F_relative)
% plot(linspace(0,simu.time(end), length(F_T(:,2))), Fpto_ws)
title('Comparison of PTO and Hydrodynamic Forces on Float')
xlabel('Time [s]'); ylabel('Force [N]')
legend('PTO Force', 'Hydrodynamic Force')
ylim([-3*10^5 3*10^5])