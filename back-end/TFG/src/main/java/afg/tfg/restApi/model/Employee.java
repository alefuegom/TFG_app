package afg.tfg.restApi.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.validation.constraints.NotEmpty;

@Entity
@Table(name="employees")
public class Employee extends User {
	
	@Column(name="name")
	@NotEmpty
	private String name;
	
	@Column(name="surname")
	@NotEmpty
	private String surname;
	
	@Column(name="dni")
	@NotEmpty
	private String dni;
	
	@Column(name="telephone")
	@NotEmpty
	private String telephone;
	
	@Column(name="qualification")
	@NotEmpty
	private String qualification;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getSurname() {
		return surname;
	}

	public void setSurname(String surname) {
		this.surname = surname;
	}

	public String getDni() {
		return dni;
	}

	public void setDni(String dni) {
		this.dni = dni;
	}

	public String getTelephone() {
		return telephone;
	}

	public void setTelephone(String telephone) {
		this.telephone = telephone;
	}

	public String getQualification() {
		return qualification;
	}

	public void setQualification(String qualification) {
		this.qualification = qualification;
	}

	
}
