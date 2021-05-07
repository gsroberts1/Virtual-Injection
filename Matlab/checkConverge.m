function L2 = checkConverge(displacedNew,displacedOld,mask)
% CHECKCONVERGE Look for change in movement of velocity vectors
% This is useful for iterative displacement correction techniques where the
% velocity fields are repeatedly reverse displaced to find a suitable
% velocity field.
% See: Thunberg P, Wigstrom L, Ebbers T, Karlsson M. JMRI, 2002;16(5):591-597.

diff = displacedNew - displacedOld; %calculate velocity movement in x,y,z
distanceMoved = sqrt(sum(diff.^2,2)); %get length
convergenceMap = reshape(distanceMoved,size(mask)); %show movements in image space
convergenceMap = convergenceMap.*mask;
L2 = mean(convergenceMap(:)); %get mean movement

end

