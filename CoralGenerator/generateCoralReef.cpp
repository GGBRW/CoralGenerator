#include <iostream>
#include <fstream>
#include <vector>
#include <CGAL/Simple_cartesian.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/IO/OBJ.h>
#include <CGAL/Aff_transformation_3.h>
#include "PerlinNoise.h"

typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_3 Point_3;
typedef Kernel::Vector_3 Vector_3;
typedef CGAL::Surface_mesh<Point_3> Mesh;
typedef CGAL::Aff_transformation_3<Kernel> Transformation;

const unsigned int terrainWidth = 4;
const unsigned int terrainHeight = 4;
const unsigned int terrainVerticesX = 64;
const unsigned int terrainVerticesY = 64;

const unsigned int numberOfCorals = 32;
std::vector<Mesh> coralMeshes;

// Perlin Noise parameters
std::vector<float> noiseFrequencies = {0.35, 0.5, 1.5};
std::vector<float> noiseAmplitudes = {1.5, 1.0, 0.2};
const unsigned int noiseSeed = 0;
PerlinNoise pn(noiseSeed);

double calculateTerrainHeight(double x, double y) {
    double z = 0.0;
    for(int i = 0; i < noiseFrequencies.size(); ++i) {
        z += noiseAmplitudes[i] * pn.noise(noiseFrequencies[i] * x, noiseFrequencies[i] * y);
    }

    return z;
}

class Coral {
public:
    Point_3 position;
    double rotation; // Rotation around Z axis
    int type; // Coral type

    Coral(const Point_3& pos, double rot, int t) : position(pos), rotation(rot), type(t) {}
};

bool readOBJ(const std::string& filename, Mesh& mesh) {
    std::ifstream input(filename);
    if (!input || !CGAL::IO::read_OBJ(input, mesh)) {
        std::cerr << "Error reading OBJ file: " << filename << std::endl;
        return false;
    }
    return true;
}

bool writeOBJ(const std::string& filename, const Mesh& mesh) {
    std::ofstream output(filename);
    if (!output || !CGAL::IO::write_OBJ(output, mesh)) {
        std::cerr << "Error writing OBJ file: " << filename << std::endl;
        return false;
    }
    return true;
}

Mesh combineMeshes(const std::vector<Coral>& corals, const Mesh& terrainMesh) {
    Mesh combinedMesh;

    // First, add all vertices and faces of the terrainMesh to the combinedMesh
    // std::map<Mesh::Vertex_index, Mesh::Vertex_index> terrainVertexMap;
    // for (auto v : terrainMesh.vertices()) {
    //     terrainVertexMap[v] = combinedMesh.add_vertex(terrainMesh.point(v));
    // }
    // for (auto f : terrainMesh.faces()) {
    //     std::vector<Mesh::Vertex_index> vertices;
    //     for (auto v : vertices_around_face(terrainMesh.halfedge(f), terrainMesh)) {
    //         vertices.push_back(terrainVertexMap[v]);
    //     }
    //     combinedMesh.add_face(vertices);
    // }

    // Add the corals
    for (const auto& coral : corals) {
        Mesh transformedMesh = coralMeshes[coral.type];

        // Apply rotation around the Y-axis
        double cos_theta = cos(coral.rotation);
        double sin_theta = sin(coral.rotation);
        Transformation rotate(CGAL::IDENTITY);
        rotate = Transformation(cos_theta, 0, sin_theta, 0, 1, 0, -sin_theta, 0, cos_theta);

        // Apply translation
        Transformation translate(CGAL::TRANSLATION, Vector_3(coral.position.x(), coral.position.y(), coral.position.z()));
        for (auto v : transformedMesh.vertices()) {
            transformedMesh.point(v) = translate(rotate(transformedMesh.point(v)));
        }

        // Add transformed vertices and faces to the combined mesh
        std::map<Mesh::Vertex_index, Mesh::Vertex_index> coralVertexMap;
        for (auto v : transformedMesh.vertices()) {
            coralVertexMap[v] = combinedMesh.add_vertex(transformedMesh.point(v));
        }
        for (auto f : transformedMesh.faces()) {
            std::vector<Mesh::Vertex_index> vertices;
            for (auto v : vertices_around_face(transformedMesh.halfedge(f), transformedMesh)) {
                vertices.push_back(coralVertexMap[v]);
            }
            combinedMesh.add_face(vertices);
        }
    }

    return combinedMesh;
}


int main() {
    // Load coral meshes 
    for(auto path : std::vector<std::string> { "./corals/cervicornis.obj", "./corals/secale.obj" }) {
        Mesh coralMesh;
        if(!readOBJ(path, coralMesh)) return 1;
        coralMeshes.push_back(coralMesh);
    }

    // Generate terrain
    Mesh terrainMesh;
    std::vector<Mesh::Vertex_index> vertexIndices;
    for (int i = 0; i < terrainVerticesX; ++i) {
        for (int j = 0; j < terrainVerticesY; ++j) {
            double x = i * (double)terrainWidth / terrainVerticesX;
            double y = j * (double)terrainHeight / terrainVerticesY;
            double z = calculateTerrainHeight(x, y);
            vertexIndices.push_back(terrainMesh.add_vertex(Point_3(x, z, y)));
        }
    }

    // Create faces for the terrain using the stored vertex indices
    for (int i = 0; i < terrainVerticesX - 1; ++i) {
        for (int j = 0; j < terrainVerticesY - 1; ++j) {
            Mesh::Vertex_index topLeft = vertexIndices[i * terrainVerticesY + j];
            Mesh::Vertex_index topRight = vertexIndices[(i + 1) * terrainVerticesY + j];
            Mesh::Vertex_index bottomLeft = vertexIndices[i * terrainVerticesY + (j + 1)];
            Mesh::Vertex_index bottomRight = vertexIndices[(i + 1) * terrainVerticesY + (j + 1)];

            terrainMesh.add_face(topLeft, bottomLeft, bottomRight);
            terrainMesh.add_face(topLeft, bottomRight, topRight);
        }
    }

    std::cout << "Generated terrain with " << terrainMesh.number_of_vertices() << " vertices" << std::endl;

    std::vector<Coral> corals;
    for(int i = 0; i < numberOfCorals; ++i) {
        double x = (double)rand() / RAND_MAX * 4.0;
        double y = (double)rand() / RAND_MAX * 4.0;
        double z = calculateTerrainHeight(x, y);
        Point_3 position(x, z, y); // Flip the z and y coordinates for OBJ purposes

        double rotation = (double)rand() / RAND_MAX * 2.0 * M_PI;

        int type = rand() % coralMeshes.size();

        corals.push_back( Coral(position, rotation, type) );
    }

    std::cout << "Generated " << numberOfCorals << " corals" << std::endl;

    Mesh combinedMesh = combineMeshes(corals, terrainMesh);

    std::cout << "Combined " << numberOfCorals << " corals into one mesh" << std::endl;

    if(!writeOBJ("terrain.obj", terrainMesh)) return 1;
    if(!writeOBJ("corals.obj", combinedMesh)) return 1;

    return 0;
}
