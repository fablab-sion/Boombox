from openscad import *
import math

                                                                     # rendering
showTube = True
cutTube = False
showRing = True
cutRing = False
showPlatesHolder = True
showElectronicPlates = True
showElectronicPlatesStandoffs = True

mmPerInch = 25.4
fn = 1000;   # facet number
eps = 0.1    # overlaps
                                                                          # tube
tubeExternalDiameter = 125
tubeInternalDiameter = 119
tubeLength = 200
tubeColour = 'DarkOrange'
                                                                    # M3 inserts
m3InsertsDiameter = 4.2
m3InsertsHeight = 6
                                                                          # ring
ringFixingHoleNb = 3
ringFixingHoleDiameter = m3InsertsDiameter
ringFixingHoleDepth = m3InsertsHeight
ringInternalDiameter = 112
ringInnerHeight = 10
ringBaseHeight = ringFixingHoleDepth + 1
ringChamferHeight = 5
ringChamferWithdrawal = ringChamferHeight/2
ringColour = 'Red'
                                                             # electronic plates
electronicPlatesLength = 3.6*mmPerInch
electronicPlatesWidth = 2.7*mmPerInch
electronicPlatesThickness = 2
electronicPlatesOffsets = [-18, 0, 16]
electronicPlatesColour = 'Green'
electronicPlatesStandoffsDiameter = 5
electronicPlatesStandoffsXDistance = 3.3*mmPerInch
electronicPlatesStandoffsYDistance = 2.4*mmPerInch
electronicPlatesStandoffsColour = 'Silver'
                                                      # electronic plates holder
platesHolderWidth = 5
platesHolderFixingHoleNb = 3
platesHolderFixingHoleDiameter = 3.5
platesHolderFixingHolesDiameter = ringInternalDiameter - 10
platesHolderFixingHoleOffsets = [-10, 10]
platesHolderColour = 'Burlywood'

# ------------------------------------------------------------------------------
                                                                # derived values
ringHeight = ringInnerHeight + ringBaseHeight
ringFixingHolesDiameter = (tubeExternalDiameter + ringInternalDiameter)/2
electronicPlateNb = len(electronicPlatesOffsets)
electronicPlatesStandoffsLength = 2*math.sqrt(
    (ringInternalDiameter/2)**2 - (electronicPlatesStandoffsYDistance/2)**2
) - electronicPlatesStandoffsDiameter
electronicPlatesStandoffsZOffset1 = (
    electronicPlatesLength - electronicPlatesStandoffsXDistance
)/2
electronicPlatesStandoffsZOffset = electronicPlatesStandoffsZOffset1 \
    - ringBaseHeight + platesHolderWidth
electronicPlatesVerticalHolderHeight = 2*electronicPlatesStandoffsZOffset1 \
    + platesHolderWidth
electronicPlatesVerticalHolderWidth = 4*electronicPlatesStandoffsZOffset1

# ------------------------------------------------------------------------------
# tube
#
                                                                          # tube
tube = difference(
    cylinder(d=tubeExternalDiameter, h=tubeLength, center=False),
    cylinder(d=tubeInternalDiameter, h=3*tubeLength, center=True)
)
                                                                        # render
tube = tube.color(tubeColour)
if showTube :
    if cutTube :
        tube = difference(
            tube,
            translate(
                cube([
                    2*tubeExternalDiameter, tubeExternalDiameter, 3*tubeLength
                ], center = True),
                [0, -tubeExternalDiameter/2, 0]
            )
        )
    tube.show()

# ------------------------------------------------------------------------------
# base ring
#
                                                                    # inner ring
ring = cylinder(d=tubeInternalDiameter, h=ringHeight, center=False)
                                                                          # base
ring = translate(
    union(
        ring,
        cylinder(d=tubeExternalDiameter, h=ringBaseHeight, center=False)
    ),
    [0, 0, -ringBaseHeight]
)
                                                                       # chamfer
ring = union(
    ring,
    translate(
        cylinder(
            d1=tubeInternalDiameter,
            d2=tubeInternalDiameter - ringChamferWithdrawal,
            h=ringChamferHeight,
            center=False
        ),
        [0, 0, ringInnerHeight - eps]
    )
)
                                                                    # inner hole
ring = difference(
    ring,
    cylinder(
        d=ringInternalDiameter,
        h=3*(ringHeight + ringChamferHeight),
        center=True
    )
)
                                                                  # fixing holes
for index in range(ringFixingHoleNb) :
    ring = difference(
        ring,
#        rotate(
            translate(
                cylinder(
                    d=ringFixingHoleDiameter,
                    h=ringFixingHoleDepth,
                    center=False
                ),
                [ringFixingHolesDiameter/2, 0, -ringBaseHeight - eps]
            ).rotate([0, 0, index/ringFixingHoleNb*360])
#            ),
#            [0, 0, index/ringFixingHoleNb*360]
#        )
    )
                                                                        # render
ring = ring.color(ringColour)
if showRing :
    if cutRing :
        ring = difference(
            ring,
            translate(
                cube([
                    2*tubeInternalDiameter,
                    tubeInternalDiameter,
                    2*ringHeight + ringChamferHeight
                ], center=False),
                [-tubeInternalDiameter, -tubeInternalDiameter, -ringHeight]
            )
        )
    ring.show()

# ------------------------------------------------------------------------------
# electronic plates
#
electronicPlate = translate(
    cube([
        electronicPlatesLength, electronicPlatesWidth, electronicPlatesThickness
    ]),
    [0, -electronicPlatesWidth/2, 0]
).rotate([0, -90, 0])
                                                                       # offsets
electronicPlates = translate(
    electronicPlate, [electronicPlatesOffsets[0], 0, 0]
)
for index in range(1, electronicPlateNb) :
    electronicPlates = union(
        electronicPlates,
        translate(
            electronicPlate,
            [electronicPlatesOffsets[index], 0, 0]
        )
    )
electronicPlates = translate(
    electronicPlates, [0, 0, -ringBaseHeight + platesHolderWidth]
)
                                                                        # render
electronicPlates = electronicPlates.color(electronicPlatesColour)
if showElectronicPlates :
    electronicPlates.show()

# ------------------------------------------------------------------------------
# electronic plates standoffs
#
electronicPlatesStandoff = translate(
    cylinder(
        d=electronicPlatesStandoffsDiameter,
        h=electronicPlatesStandoffsLength,
        fn = 6,
        center=False
    ).rotate([0, 90, 0]),
    [-electronicPlatesStandoffsLength/2, 0, 0]
)
                                                                       # offsets
electronicPlatesStandoffs = translate(
    electronicPlatesStandoff,
    [0, -electronicPlatesStandoffsYDistance/2, 0]
)
electronicPlatesStandoffs  = union(
    electronicPlatesStandoffs,
    translate(
        electronicPlatesStandoff,
        [0, electronicPlatesStandoffsYDistance/2, 0]
    )
)
electronicPlatesStandoffs  = translate(
    electronicPlatesStandoffs,
    [0, 0, electronicPlatesStandoffsZOffset]
)
                                                                        # render
electronicPlatesStandoffs = electronicPlatesStandoffs.color(
    electronicPlatesStandoffsColour
)
if showElectronicPlatesStandoffs :
    electronicPlatesStandoffs.show()

# ------------------------------------------------------------------------------
# electronic plates holder
#
                                                                    # base plate
platesHolder = cylinder(
    d=ringInternalDiameter, h=platesHolderWidth, center=False
)
                                                                  # fixing holes
for index in range(platesHolderFixingHoleNb) :
    platesHolder = difference(
        platesHolder,
        translate(
            cylinder(
                d=platesHolderFixingHoleDiameter,
                h=3*platesHolderWidth,
                center=True
            ),
            [platesHolderFixingHolesDiameter/2, 0, 0]
        ).rotate([0, 0, index/platesHolderFixingHoleNb*360 + 60])
    )
                                                              # vertical holders
for xOffset in platesHolderFixingHoleOffsets :
    for ySide in [-1, 1] :
        platesHolder = union(
            platesHolder,
            translate(
                cube([
                    platesHolderWidth,
                    electronicPlatesVerticalHolderWidth,
                    electronicPlatesVerticalHolderHeight
                ]),
                [
                    xOffset - platesHolderWidth/2,
                    ySide*electronicPlatesStandoffsYDistance/2
                        - (1 - ySide)/2*electronicPlatesVerticalHolderWidth,
                    0
                ]
            )
        )
                                                                        # render
platesHolder = translate(platesHolder, [0, 0, -ringBaseHeight])
platesHolder = platesHolder.color(platesHolderColour)
if showPlatesHolder :
    platesHolder.show()
