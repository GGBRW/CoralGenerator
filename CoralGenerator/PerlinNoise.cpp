#include "PerlinNoise.h"
#include <cmath>
#include <numeric>
#include <algorithm>
#include <random>

PerlinNoise::PerlinNoise(unsigned int seed) {
    // Initialize the permutation vector with the values 0 to 255
    p.resize(256);
    std::iota(p.begin(), p.end(), 0);
    // Shuffle the elements using the provided seed
    std::default_random_engine engine(seed);
    std::shuffle(p.begin(), p.end(), engine);
    // Duplicate the vector to avoid overflow
    p.insert(p.end(), p.begin(), p.end());
}

double PerlinNoise::noise(double x, double y) const {
    int X = (int)std::floor(x) & 255;
    int Y = (int)std::floor(y) & 255;

    x -= std::floor(x);
    y -= std::floor(y);

    double u = fade(x);
    double v = fade(y);

    int aa = p[p[X] + Y];
    int ab = p[p[X] + Y + 1];
    int ba = p[p[X + 1] + Y];
    int bb = p[p[X + 1] + Y + 1];

    double res = lerp(v, lerp(u, grad(aa, x, y), grad(ba, x - 1, y)),
                            lerp(u, grad(ab, x, y - 1), grad(bb, x - 1, y - 1)));
    return (res + 1.0) / 2.0; // Transform to [0, 1] range
}

double PerlinNoise::fade(double t) {
    // Fade function as defined by Ken Perlin
    // 6t^5 - 15t^4 + 10t^3
    return t * t * t * (t * (t * 6 - 15) + 10);
}

double PerlinNoise::lerp(double t, double a, double b) {
    // LERP = Linear interpolation
    return a + t * (b - a);
}

double PerlinNoise::grad(int hash, double x, double y) {
    // Convert low 3 bits of hash code into 8 simple gradient directions
    int h = hash & 7;
    double u = h < 4 ? x : y;
    double v = h < 4 ? y : x;
    // and compute the dot product with (x,y)
    return ((h & 1) ? -u : u) + ((h & 2) ? -2.0 * v : 2.0 * v);
}
