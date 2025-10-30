%% Objective functions

P_Tstall = max(P_T(:,2))/100000;                % Tank stall pressure [Pa]
Fstop_High_tot = sum(Fstop_High(:,2));          % Cumulative high endstop force [N]
Fstop_Low_tot = sum(Fstop_Low(:,2));            % Cumulative low endstop force [N]
Fstop_tot = Fstop_High_tot + Fstop_Low_tot;     % Cumulative endstop force [N]