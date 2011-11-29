import sbt._
import com.github.retronym.OneJarProject

class Project(info: ProjectInfo) extends DefaultProject(info) with IdeaProject with OneJarProject { 

//  override def mainClass = Some("org.foo.MainObj")

  // Scala unit testing
  val scalatest = "org.scalatest" % "scalatest" % "1.3"

  // Store all slick2d jar files in own directory under lib/
  def slick2dJars = descendents("lib" / "slick2d", "*.jar")

  // Simplex libs
//  def simplex3dJars = descendents("lib" / "simplex3d", "*.jar")

  override def unmanagedClasspath = super.unmanagedClasspath +++ slick2dJars

  
}
