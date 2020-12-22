package alefuegom.tfg.model;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;


@Entity
@Table(name="empresas")
public class Empresa extends BaseEntity{

	@NotBlank
	private String name;
	
	@NotBlank
	@Column(unique=true)
	@Pattern(regexp = "[\\w]{1}[\\d]{8}((^|)([\\w]{1}|[\\d]{1}))")
	private String cif;
	
	@NotBlank
	private String direccion;
	
	@NotNull
	private int telefono;
	
	@NotBlank
	@Pattern(regexp = "[\\w]{2}[\\d]{22}")
	private String cuentaBancaria;
	
	@OneToOne(cascade= CascadeType.ALL)
	private Usuario usuario;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getCif() {
		return cif;
	}

	public void setCif(String cif) {
		this.cif = cif;
	}

	public String getDireccion() {
		return direccion;
	}

	public void setDireccion(String direccion) {
		this.direccion = direccion;
	}

	public int getTelefono() {
		return telefono;
	}

	public void setTelefono(int telefono) {
		this.telefono = telefono;
	}

	public String getCuentaBancaria() {
		return cuentaBancaria;
	}

	public void setCuentaBancaria(String cuentaBancaria) {
		this.cuentaBancaria = cuentaBancaria;
	}

	public Usuario getUsuario() {
		return usuario;
	}

	public void setUsuario(Usuario usuario) {
		this.usuario = usuario;
	}
	
	
	
	

}
