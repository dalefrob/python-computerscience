//---------------------------Draw Rays and Walls--------------------------------

// Calculates the perpendicular distance from point (ax,ay) to point (bx,by),
// corrected for the viewing angle. This "projects" the distance onto the
// player's forward-facing axis to avoid the fisheye effect later.
float perpendicularDistance(float startX, float startY, float endX, float endY, float angleDeg)
{
    return cos(degToRad(angleDeg)) * (endX - startX) 
         - sin(degToRad(angleDeg)) * (endY - startY);
}

void drawRays2D()
{
    // Draw the ceiling (top half of 3D viewport) in cyan
    glColor3f(0, 1, 1);
    glBegin(GL_QUADS);
        glVertex2i(526,   0); glVertex2i(1006,   0);
        glVertex2i(1006, 160); glVertex2i(526,  160);
    glEnd();

    // Draw the floor (bottom half of 3D viewport) in blue
    glColor3f(0, 0, 1);
    glBegin(GL_QUADS);
        glVertex2i(526,  160); glVertex2i(1006, 160);
        glVertex2i(1006, 320); glVertex2i(526,  320);
    glEnd();

    // --- Ray casting variables ---
    int   rayIndex,          // current ray number (0–59)
          mapTileX,          // X index of the current map tile being tested
          mapTileY,          // Y index of the current map tile being tested
          mapTileIndex,      // flat (1D) index into the map array
          depthOfField,      // how many tile steps we've marched along this ray
          hitSide;           // which wall face was hit (unused visually here, reserved)

    float vertHitX, vertHitY,   // world coords where the vertical-wall ray hit
          rayX, rayY,           // current ray tip position during DDA march
          rayAngle,             // angle of the current ray being cast
          stepX, stepY,         // how far to step each DDA iteration
          distToVertWall,       // corrected distance to nearest vertical wall hit
          distToHorizWall;      // corrected distance to nearest horizontal wall hit

    // Start the first ray 30° to the left of the player's facing direction,
    // so the 60-ray fan is centered on where the player is looking.
    rayAngle = FixAng(pa + 30);

    for (rayIndex = 0; rayIndex < 60; rayIndex++)
    {
        // -------------------------------------------------------
        // VERTICAL WALL CHECK
        // Cast the ray to find the nearest vertical grid line (x-aligned boundary).
        // In a 64-pixel tile grid every multiple of 64 is a vertical boundary.
        // -------------------------------------------------------
        depthOfField  = 0;
        distToVertWall = 100000;          // sentinel — "no hit yet"
        float slopeTan = tan(degToRad(rayAngle));

        if (cos(degToRad(rayAngle)) > 0.001)
        {
            // Ray faces RIGHT → first boundary is the right edge of the player's tile
            rayX  = (((int)px >> 6) << 6) + 64;  // snap to next vertical grid line
            rayY  = (px - rayX) * slopeTan + py;  // matching Y on the ray
            stepX =  64;
            stepY = -stepX * slopeTan;
        }
        else if (cos(degToRad(rayAngle)) < -0.001)
        {
            // Ray faces LEFT → first boundary is the left edge of the player's tile
            rayX  = (((int)px >> 6) << 6) - 0.0001; // just inside the left boundary
            rayY  = (px - rayX) * slopeTan + py;
            stepX = -64;
            stepY = -stepX * slopeTan;
        }
        else
        {
            // Ray is perfectly vertical (90° or 270°) — can never hit a vertical wall
            rayX = px; rayY = py;
            depthOfField = 8;              // skip the march entirely
        }

        // DDA march: step along vertical grid lines until we hit a wall or give up
        while (depthOfField < 8)
        {
            mapTileX     = (int)(rayX) >> 6;          // tile col  (divide by 64)
            mapTileY     = (int)(rayY) >> 6;          // tile row
            mapTileIndex = mapTileY * mapX + mapTileX; // flat index into map[]

            if (mapTileIndex > 0 && mapTileIndex < mapX * mapY && map[mapTileIndex] == 1)
            {
                // Hit a wall tile — record distance and stop marching
                depthOfField   = 8;
                distToVertWall = perpendicularDistance(px, py, rayX, rayY, rayAngle);
            }
            else
            {
                // Empty tile — step to the next vertical boundary
                rayX += stepX;
                rayY += stepY;
                depthOfField++;
            }
        }

        // Save the vertical-wall hit position so we can draw the 2D ray later
        vertHitX = rayX;
        vertHitY = rayY;

        // -------------------------------------------------------
        // HORIZONTAL WALL CHECK
        // Cast the ray to find the nearest horizontal grid line (y-aligned boundary).
        // -------------------------------------------------------
        depthOfField    = 0;
        distToHorizWall = 100000;
        slopeTan        = 1.0 / slopeTan;   // reciprocal: now dx/dy instead of dy/dx

        if (sin(degToRad(rayAngle)) > 0.001)
        {
            // Ray faces UP (in screen space) → first boundary is above the player's tile
            rayY  = (((int)py >> 6) << 6) - 0.0001;  // just above the top boundary
            rayX  = (py - rayY) * slopeTan + px;
            stepY = -64;
            stepX = -stepY * slopeTan;
        }
        else if (sin(degToRad(rayAngle)) < -0.001)
        {
            // Ray faces DOWN → first boundary is the bottom edge of the player's tile
            rayY  = (((int)py >> 6) << 6) + 64;
            rayX  = (py - rayY) * slopeTan + px;
            stepY =  64;
            stepX = -stepY * slopeTan;
        }
        else
        {
            // Ray is perfectly horizontal — can never hit a horizontal wall
            rayX = px; rayY = py;
            depthOfField = 8;
        }

        // DDA march along horizontal grid lines
        while (depthOfField < 8)
        {
            mapTileX     = (int)(rayX) >> 6;
            mapTileY     = (int)(rayY) >> 6;
            mapTileIndex = mapTileY * mapX + mapTileX;

            if (mapTileIndex > 0 && mapTileIndex < mapX * mapY && map[mapTileIndex] == 1)
            {
                depthOfField    = 8;
                distToHorizWall = perpendicularDistance(px, py, rayX, rayY, rayAngle);
            }
            else
            {
                rayX += stepX;
                rayY += stepY;
                depthOfField++;
            }
        }

        // -------------------------------------------------------
        // CHOOSE CLOSER HIT & DRAW 2D RAY
        // -------------------------------------------------------

        // Default: horizontal wall hit (brighter green)
        glColor3f(0, 0.8, 0);

        if (distToVertWall < distToHorizWall)
        {
            // Vertical wall was actually closer — use that hit point (darker green
            // so the player can visually distinguish N/S from E/W walls)
            rayX            = vertHitX;
            rayY            = vertHitY;
            distToHorizWall = distToVertWall;
            glColor3f(0, 0.6, 0);
        }

        // Draw the 2D ray line on the mini-map
        glLineWidth(2);
        glBegin(GL_LINES);
            glVertex2i(px, py);   // ray origin: player position
            glVertex2i(rayX, rayY); // ray end: wall hit point
        glEnd();

        // -------------------------------------------------------
        // DRAW 3D WALL SLICE
        // -------------------------------------------------------

        // Fisheye correction: rays at the edge of the FOV travel farther than
        // the center ray for the same wall. Multiplying by cos(angle offset)
        // projects them back onto the flat view plane.
        int angleDelta   = FixAng(pa - rayAngle);
        distToHorizWall  = distToHorizWall * cos(degToRad(angleDelta));

        // Wall slice height is inversely proportional to distance
        // (mapS is the tile size in pixels, 320 is the viewport height)
        int wallSliceHeight = (mapS * 320) / distToHorizWall;
        if (wallSliceHeight > 320) wallSliceHeight = 320;   // clamp to viewport

        // Centre the slice vertically (160 = half of 320-pixel viewport height)
        int wallSliceTop = 160 - (wallSliceHeight >> 1);

        // Draw the vertical wall slice in the 3D viewport.
        // Each of the 60 rays occupies an 8-pixel-wide column starting at x=530.
        glLineWidth(8);
        glBegin(GL_LINES);
            glVertex2i(rayIndex * 8 + 530, wallSliceTop);
            glVertex2i(rayIndex * 8 + 530, wallSliceTop + wallSliceHeight);
        glEnd();

        // Advance to the next ray (sweep right-to-left through the 60° FOV)
        rayAngle = FixAng(rayAngle - 1);
    }
}//-----------------------------------------------------------------------------

// Key techniques

// DDA (Digital Differential Analysis) 
// — instead of testing every pixel, the march jumps exactly from one grid line to the next, making it fast.
// Bit-shift tile snapping (>> 6 = divide by 64, << 6 = multiply by 64)
//  — quickly aligns coordinates to the 64×64 tile grid.
// Fisheye correction
//  — without the cos(angleDelta) multiplication, walls would appear curved because edge rays travel farther than center rays.
// Shade differentiation
//  — vertical walls are drawn in darker green than horizontal ones, giving a cheap but effective sense of depth and direction.